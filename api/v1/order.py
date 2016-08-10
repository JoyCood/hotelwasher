#!/usr/bin/python
# -*- coding: utf-8 -*-

from model.member.main import Member 
from model.member.mix import Member_Mix
from model.order.main import Order
from protocol.v1 import order_pb2
from config import (mapper, base)
from bson.objectid import ObjectId 
from server import(
        add_online_washer,
        get_online_washer_by_phone, 
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
    unpack_data = order_pb2.Place_Order_Request()
    unpack_data.ParseFromString(data)
    
    order_type = unpack_data.type #普通｜专业
    total      = unpack_data.total
    city       = unpack_data.city.strip().encode('utf-8')
    longitude  = unpack_data.longitude #经度
    latitude   = unpack_data.latitude  #纬度
    address    = unpack_data.address.strip()
    price = 88 
    now = int(time.time())
    
    pack_data = order_pb2.Place_Order_Response()

    member = get_online_customer_by_socket(socket)

    washer = washer_allocate(city, longitude, latitude)
    
    if washer:
        doc = {
            "customer_phone": '+8618565389757',
            "washer_phone": washer['phone'],
            "total": total,
            "price": price,
            "order_status": order_pb2.DISTRIBUTED,
            "order_type": order_type,
            "place_time": now,
            "city": city,
            "address": address,
            "discount": 0,
            "cancel_by": 0,
            "feedback": 0,
            "score": 0,
            "longitude": longitude,
            "latitude": latitude
        }
        res = Order.insert_one(doc)
        pack_data.order_id     = str(res.inserted_id)
        pack_data.order_type   = order_type
        pack_data.total        = total
        pack_data.price        = price
        pack_data.washer.id    = washer['id']
        pack_data.washer.phone = washer['nick']
        pack_data.washer.level = washer['level']
        pack_data.washer.longitude = washer['longitude']
        pack_data.washer.latitude = washer['latitude']
        pack_data.error_code = order_pb2.SUCCESS
        
        customer = {
                "phone": '+8618565389757', 
                "order_id": str(res.inserted_id),
                "longitude": longitude,
                "latitude": latitude,
                "order_status": 1
        }
        
        washer['customer'] = customer
        add_online_washer(washer)
        common.send(socket, order_pb2.PLACE_ORDER, pack_data)

        pack_data = order_pb2.Allocate_Order_Response()
        pack_data.order_id = str(res.inserted_id)
        pack_data.customer_phone = '+8618565389757'
        pack_data.error_code = order_pb2.SUCCESS
        common.send(washer['socket'], order_pb2.ALLOCATE_ORDER, pack_data)
        return

    pack_data.error_code = order_pb2.ERROR_WASHER_NOT_FOUND
    common.send(socket, order_pb2.PLACE_ORDER, pack_data)
    
def washer_allocate(city, longitude, latitude):
    md5 = hashlib.md5()
    md5.update(city)
    city = md5.hexdigest()

    exploder = ' '
    cmd = ['GEORADIUS']
    cmd.append(city)
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
    print washers, size,index
    washer = washers[index]

    phone     = washer[0]
    distance  = washer[1]
    longitude = float(washer[2][0])
    latitude  = float(washer[2][1])
    
    #common.redis.zrem(city, phone)
    print phone 
    washer = get_online_washer_by_phone(phone)

    washer['customer']  = phone
    washer['longitude'] = longitude
    washer['latitude']  = latitude

    return washer

def history_order(socket, data):
    unpack_data = order_pb2.History_Order_Request()
    unpack_data.ParseFromString(data)


def feedback(socket, data):
    """ 订单评分"""
    pass

def pay(socket, data):
    pass
