#!/usr/bin/python
# -*- coding: utf-8 -*-

from model.member.main import Member 
from model.member.mix import Member_Mix
from protocol.v1 import order_pb2
from config import (mapper, base)
from bson.objectid import ObjectId 

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
    total      = unpack_data.total
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

