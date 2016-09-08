#!/usr/bin/python
# -*- coding: utf-8 -*-

from model.member.main import Member 
from model.member.mix import Member_Mix
from model.washer.main import Washer
from model.order.main import Order
from protocol.v1 import order_pb2
from config import (mapper, base)
from bson.objectid import ObjectId 
from server import(
        add_online_washer,
        get_online_washer_by_phone, 
        get_online_washer_by_socket,
        get_online_customer_by_phone,
        get_online_customer_by_socket)

import common
import phonenumbers

import sys
import hashlib
import time
import random

def handle(socket, protocol, data):
    handler = mapper.handler.get(protocol)
    if handler is None:
        print 'handler not found'
        return
    fun = getattr(sys.modules[__name__], handler)
    fun(socket, data)

def place_order(socket, data):
    """ 下单
      - socket
      - data
    """
    pack_data = order_pb2.Place_Order_Response()
    
    member = get_online_customer_by_socket(socket)
    
    if member is None:
        pack_data.error_code = order_pb2.ERROR_NOT_LOGGIN
        common.send(socket, order_pb2.PLACE_ORDER, pack_data)
        return

    unpack_data = order_pb2.Place_Order_Request()
    unpack_data.ParseFromString(data)
    
    order_type = unpack_data.type      #普通｜专业
    quantity   = unpack_data.quantity  #数量
    city_code  = unpack_data.city_code #城市代码
    longitude  = unpack_data.longitude #经度
    latitude   = unpack_data.latitude  #纬度
    address    = unpack_data.address.strip() #下单所在地
    price      = 88 
    now        = int(time.time())
    
    washer = washer_allocate(city_code, longitude, latitude, order_type)
    
    if washer:
        doc = {
            "customer_phone": member['phone'], #客户号码
            "washer_phone": washer['phone'], #商家号码
            "washer_nick": washer['nick'], #商家昵称
            "quantity": quantity, #数量
            "price": price, #价格
            "order_status": order_pb2.DISTRIBUTED, #订单状态,默认已分配
            "order_type": order_type, #普通洗还是专业洗
            "order_time": now, #下单时间
            "city_code": city_code, #城市代码
            "address": address, #下单所在地
            "discount": 0, #折扣
            "cancel_by": 0, #订单被谁取消
            "cancel_reason": list(), #取消的原因
            "cancel_time": 0, #取消时间
            "washer_score": 0, #商家获得评分
            "customer_score": 0, #客户获得评分
            "longitude": longitude, #客户下单时所处经度
            "latitude": latitude #客户下单时所处纬度
        }
        res = Order.insert_one(doc)

        #通知用户下单成功
        pack_data.order_id     = str(res.inserted_id)
        pack_data.order_type   = order_type
        pack_data.quantity     = total
        pack_data.price        = price
        pack_data.washer.id    = washer['id']
        pack_data.washer.phone = washer['phone']
        pack_data.washer.nick  = washer['nick']
        pack_data.washer.level = washer['level']
        pack_data.washer.longitude = washer['longitude']
        pack_data.washer.latitude = washer['latitude']
        pack_data.error_code = order_pb2.SUCCESS
        common.send(socket, order_pb2.PLACE_ORDER, pack_data)

        #通知商家系统分配订单
        pack_data = order_pb2.Allocate_Order_Response()
        pack_data.order_id = str(res.inserted_id)
        pack_data.customer_phone = member['phone']
        pack_data.error_code = order_pb2.SUCCESS
        common.send(washer['socket'], order_pb2.ALLOCATE_ORDER, pack_data)
        return

    pack_data.error_code = order_pb2.ERROR_WASHER_NOT_FOUND
    common.send(socket, order_pb2.PLACE_ORDER, pack_data)
    
def customer_cancel_order(socket, data):
    """ 用户取消订单 
      - socket
      - data
    """
    pack_data = order_pb2.Cancel_Order_Response()

    member = get_online_customer_by_socket(socket)

    if member is None:
        pack_data.error_code = order_pb2.ERROR_NOT_LOGGIN
        common.send(socket, order_pb2.CUSTOMER_CANCEL_ORDER, pack_data)
        return
        
    unpack_data = order_pb2.Cancel_Order_Request()
    unpack_data.ParseFromString(data)

    order_id = unpack_data.order_id.strip()
    reason   = unpack_data.reason.strip()

    filter = {    
        "_id": ObjectId(order_id),
        "customer_phone": member['phone'],
        "order_status": order_pb2.DISTRIBUTED
    }

    order = Order.find_one(filter)
    if order is None:
        pack_data.error_code = order_pb2.ERROR_ORDER_NOT_FOUND
        common.send(socket, order_pb2.CUSTOMER_CANCEL_ORDER, pack_data)
        return

    update = {
        "$set": {
            "cancel_reason": reason,
            "cancel_by": order_pb2.CUSTOMER,
            "cancel_time": int(time.time())
        }        
    }

    res = Order.update_one(filter, update)
    pack_data.error_code = order_pb2.SUCCESS
    common.send(socket, order_pb2.CUSTOMER_CANCEL_ORDER, pack_data)

    washer = get_online_washer_by_phone(order['washer_phone'])
    pack_data.error_code = order_pb2.ERROR_ORDER_CANCELED
    common.send(washer['socket'], order_pb2.CUSTOMER_CANCEL_ORDER, pack_data)

def washer_cancel_order(socket, data):
    """ 商家取消订单 
      - socket
      - data
    """
    pack_data = order_pb2.Cancel_Order_Response()

    washer = get_online_washer_by_socket(socket)

    if washer is None:
        pack_data.error_code = order_pb2.ERROR_NOT_LOGGIN
        common.send(socket, order_pb2.WASHER_CANCEL_ORDER, pack_data)
        return
        
    unpack_data = order_pb2.Cancel_Order_Request()
    unpack_data.ParseFromString(data)

    order_id = unpack_data.order_id.strip()
    reason   = unpack_data.reason.strip()

    filter = {    
        "_id": ObjectId(order_id),
        "washer_phone": washer['phone']
    }

    order = Order.find_one(filter)
    if order is None:
        pack_data.error_code = order_pb2.ERROR_ORDER_NOT_FOUND
        common.send(socket, order_pb2.WASHER_CANCEL_ORDER, pack_data)
        return

    update = {
        "$set": {
            "cancel_reason": reason,
            "cancel_by": order_pb2.WASHER,
            "cancel_time": int(time.time())
        }        
    }

    res = Order.update_one(filter, update)
    pack_data.error_code = order_pb2.SUCCESS
    common.send(socket, order_pb2.WASHER_CANCEL_ORDER, pack_data)

    customer = get_online_customer_by_phone(order['customer_phone'])
    pack_data.error_code = order_pb2.ERROR_ORDER_CANCELED
    common.send(customer['socket'], order_pb2.WASHER_CANCEL_ORDER, pack_data)

def delivered(socket, data):
    """ 取件 
      - socket
      - data
    """
    pack_data = order_pb2.Delivered_Response()
    washer = get_online_washer_by_socket(socket)
    if washer is None:
        pack_data.error_code = order_pb2.ERROR_NOT_LOGGIN
        common.send(socket, order_pb2.DELIVERED, pack_data)
        return
    unpack_data = order_pb2.Delivered_Request()
    unpack_data.ParseFromString(data)

    order_id = unpack_data.order_id.strip();
    filter = {
        "_id": ObjectId(order_id),
        "washer_phone": washer['phone'],
        "order_status": order_pb2.DISTRIBUTED
    }
    order = Order.find_one(filter)
    if order is None:
        pack_data.error_code = order_pb2.ERROR_ORDER_NOT_FOUND
        common.send(socket, order_pb2.DELIVERED, pack_data)
        return
    update = {
        "$set": {
            "order_status": order_pb2.DELIVERED    
        }        
    }
    res = Order.update_one(filter, update)
    if res['modified_count'] == 0:
        pack_data.error_code = order_pb2.ERROR_DELIVERED_FAILURE
        common.send(socket, order_pb2.DELIVERED, pack_data)
        return
    pack_data.error_code = order_pb2.SUCCESS
    common.send(socket, order_pb2.DELIVERED, pack_data)

    #todo:通知用户订单状态发生变化

def washer_allocate(city_code, longitude, latitude, order_type):
    """ 给下单用户分配商家
      - city_code 城市代码
      - longitude 经度
      - latitude  纬度
    """
    key = str(city_code) + '-' + order_type;

    exploder = ' '
    cmd = ['GEORADIUS']
    cmd.append(key)
    cmd.append(str(longitude))
    cmd.append(str(latitude))
    cmd.append('3 km WITHDIST WITHCOORD')
    cmd = exploder.join(cmd)

    washers = common.redis.execute_command(cmd)

    if washers is None:
        return

    size = len(washers)
    if not size:
        return
    
    index = random.randint(0, size-1)
    washer = washers[index]

    phone     = washer[0]
    distance  = washer[1]
    longitude = float(washer[2][0])
    latitude  = float(washer[2][1])
    
    #common.redis.zrem(city, phone)
    washer = get_online_washer_by_phone(phone)

    washer['phone']     = phone
    washer['longitude'] = longitude
    washer['latitude']  = latitude

    return washer

def history_order(socket, data):
    """ 历史订单
     - socket
     - data
    """
    pack_data = order_pb2.Order_List_Response()
    
    member = get_online_customer_by_socket(socket)
    if member is None:
        pack_data.error_code = order_pb2.ERROR_NOT_LOGGIN
        common.send(sock, order_pb2.ORDER_LIST, pack_data)
        return

    unpack_data = order_pb2.Order_List_Request()
    unpack_data.ParseFromString(data)

    offset = unpack_data.offset
    limit  = unpack_data.limit
    filter = {
        "customer_phone": member['phone'],
        "order_time": {
            "$lt": offset    
        }
    }
    sort   = [("order_time", -1)]}
    cursor = Order.find(filter, sort=sort, limit=limit)

    for item in cursor:
        filter = {"phone":item['washer_phone']}
        washer = Washer.find_one(filter)
        if washer is None:
            continue
        order = pack_data.order.add()
        order.order_id = str(item['_id'])
        order.order_status = item['order_status']
        order.quantity = item['quantity']
        order.order_time = item['order_time']
        order.washer_id = str(washer['_id'])
        order.washer_nick = washer['nick']
    common.send(socket, order_pb2.ORDER_LIST, pack_data)

def customer_feedback(socket, data):
    """ 用户对订单评分
      - socket
      - data
    """
    pass
    
def washer_feedback(socket, data):
    """ 商家对订单打分 
      - socket
      - data
    """
    pass

def estimates(socket, data):
    """ 估价 """
    pass
