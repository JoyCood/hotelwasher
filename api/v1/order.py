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
    unpack_data = Place_Order_Request()
    unpack_data.ParseFromString(data)

    phone     = unpack_data.phone.strip()
    secret    = unpack_data.secret.strip()
    type      = unpack_data.type
    total     = unpack_data.total
    longitude = unpack_data.longitude #经度
    latitude  = unpack_data.latitude  #纬度
    address   = unpack_data.address.strip()
    filter = [
        { "$geonear": {
            "near": {"type":"Point", "coordinates":[longitude, latitude]},                   "" 
            "limit": base.WASHER_MAX_RETURN,
            "maxDistance": base.WASHER_MAX_DISTANCE,
            "spherical": True,
            "distanceField": "distance"
        }}
    ]
    

