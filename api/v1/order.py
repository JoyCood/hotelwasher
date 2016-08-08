#!/usr/bin/python
# -*- coding: utf-8 -*-

from model.member.main import Member 
from model.member.mix import Member_Mix
from protocol.v1 import order_pb2
from config import (mapper, base)
from bson.objectid import ObjectId 
from server import(get_online_customer_by_socket)

import common
import phonenumbers

import sys
import hashlib
import time

def handle(socket, protocol, data):
    handler = mapper.handler.get(protocol)
    if handler is None:
        print 'handler not found'
        return
    fun = getattr(sys.modules[__name__], handler)
    fun(socket, data)

def place_order(socket, data):
    unpack_data = order_pb2.Place_Order_Request()
    unpack_data.ParseFromString(data)

    phone      = unpack_data.phone.strip()
    signature  = unpack_data.secret.strip()
    order_type = unpack_data.type #普通｜专业
    type       = unpack_data.total
    city       = unpack_data.city
    longitude  = unpack_data.longitude #经度
    latitude   = unpack_data.latitude  #纬度
    address    = unpack_data.address.strip()
    
    washers = find_near_washer(city, longitude, latitude)
    
    size = len(washers)
    
    if size:
        index = random.randint(0, size)
        washer = washers[index]
        redis.zrem(city, washer)
        pack_data.washer.id = washer['id']
        pack_data.washer.phone = washer['nick']
        pack_data.washer.level = washer['level']
        pack_data.washer.longitude = washer['longitude']
        pack_data.washer.latitude = washer['latitude']
        doc = {
            "phone": phone,
            "washer_id": washer['nick'],
            "total": total,
            "city": city,
            "address": address,
            "type": type,
            "create_time": now,
            "status": 0
        }
        Order.insert_one()
        common.send(socket, washer_pb2.Place_Order_Request, pack_data)
        return

    pack_data.error_code = washer_pb2.ERROR_WASHER_NOT_FOUND
    common.send(socket, washer_pb2.Place_Order_Request, pack_data)
    
def history_order(socket, data):
    unpack_data = order_pb2.History_Order_Request()
    unpack_data.ParseFromString(data)

def order_check(socket, data):
    member = get_online_customer_by_socket(socket)
    if member is None:
        return
    
    pack_data = order_pb2. Order_List_Response()
    filter = {
        "customer":member['phone'], 
        "feedback":0}
    }

    orders = Order.find(filter)
     
    for item in orders:
        order = pack_data.order.add()
        order.id = str(item['id'])
        order.customer = item['customer']
        order.price = item['price']
        order.order_status = item['order_status']
        order.order_type = item['order_type']
        order.order_time = item['order_time']
        order.customer_type = item['order_type']
        
        if item['washer'] and item['order_status']==order_pb2.DISTRIBUTED and item['cancel_by']==0: #已派发
            #返回商家信息
        elif item['order_status']==order_pb2.RESTORED and item['pay_status'] == order_pb2.WAIT_PAY: #未支付
            #返回订单信息
        

    if orders:
        common.send(socket, order_pb2.UNFINISH_ORDER, pack_data)


def feedback(socket, data):
    """ 订单评分"""
    pass

def pay(socket, data):
    pass
