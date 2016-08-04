#!/usr/bin/python
# -*- coding: utf-8 -*-

from model.washer.main import Washer
from model.washer.mix  import Washer_Mix
from protocol.v1 import washer_pb2
from config import (mapper, base)
from helper import helper
from bson.objectid import ObjectId 
from pymongo.errors import DuplicateKeyError
from server import (
        add_online_washer, 
        get_online_washer, 
        get_online_washer_by_socket)

from redis.exceptions import ResponseError

import common

import sys
import hashlib
import random
import time

def handle(socket, protocol, data):
    handler = mapper.handler.get(protocol)
    if handler is None:
        print 'handler not found'
        return
    fun = getattr(sys.modules[__name__], handler)
    fun(socket, data)

def login(socket, data):
    unpack_data = washer_pb2.Login_Request()
    unpack_data.ParseFromString(data)

    phone = unpack_data.phone.strip()
    password = unpack_data.password.strip()

    washer_id = unpack_data.washer_id.strip()
    signature = unpack_data.signature.strip()
    
    md5 = hashlib.md5()
    md5.update(password)
    password = md5.hexdigest();

    pack_data = washer_pb2.Login_Response()
    
    if not helper.verify_phone(phone):
        pack_data.error_code = washer_pb2.ERROR_PHONE_INVALID
        common.send(socket, washer_pb2.LOGIN, pack_data)
        print 'phone invalid'
        return
    filter = {
        "phone": phone        
    }

    washer = Washer.find_one(filter)
    if washer is None:
        pack_data.error_code = washer_pb2.ERROR_WASHER_NOT_FOUND
        common.send(socket, washer_pb2.LOGIN, pack_data)
        print 'washer not found'
        return
    elif washer['password'] != password:
        pack_data.error_code = washer_pb2.ERROR_PASSWORD_INVALID
        common.send(socket, washer_pb2.LOGIN, pack_data)
        print 'password invalid'
        return 
    
    pack_data.washer.id = str(washer['_id'])
    pack_data.washer.nick = washer['nick']
    pack_data.washer.phone = washer['phone']
    pack_data.washer.avatar_small = washer['avatar_small']
    pack_data.washer.avatar_mid = washer['avatar_mid']
    pack_data.washer.avatar_big = washer['avatar_big']
    pack_data.washer.level = washer['level']
    pack_data.washer.status = washer['status']
    pack_data.error_code = washer_pb2.SUCCESS
    common.send(socket, washer_pb2.LOGIN, pack_data)
    washer['socket'] = socket
    add_online_washer(washer)

def register(socket, data):
    unpack_data = washer_pb2.Register_Request()
    unpack_data.ParseFromString(data)

    nick  = unpack_data.nick.strip()
    phone = unpack_data.phone.strip()
    avatar_small = unpack_data.avatar_small.strip()
    avatar_mid   = unpack_data.avatar_mid.strip()
    avatar_big   = unpack_data.avatar_big.strip()
    password = unpack_data.password.strip()
    confirm_password = unpack_data.confirm_password.strip()
    authcode = unpack_data.authcode
    signature = unpack_data.signature.strip()

    pack_data = washer_pb2.Register_Response()

    if password != confirm_password:
        pack_data.error_code = washer_pb2.ERROR_PASSWORD_NOT_EQUAL
        common.send(socket, washer_pb2.REGISTER, pack_data)
        print 'password not equal'
        return
    elif not helper.verify_phone(phone):
        pack_data.error_code = washer_pb2.ERROR_PHONE_INVALID
        common.send(socket, washer_pb2.REGISTER, pack_data)
        print 'phone invalid'
        return

    now = int(time.time())
    filter = {"phone":phone}
    washer = Washer.find_one(filter)
    washer_mix = Washer_Mix.find_one(filter)
    
    if washer is not None:
        pack_data.error_code = washer_pb2.ERROR_WASHER_EXIST
        common.send(socket, washer_pb2.REGISTER, pack_data)
        print 'washer exist'
        return
    elif washer_mix is None or washer_mix['authcode'] != authcode:
        pack_data.error_code = washer_pb2.ERROR_AUTHCODE_INVALID
        common.send(socket, washer_pb2.REGISTER, pack_data)
        print 'authcode invalid'
        return
    elif washer_mix['expired'] < now:
        pack_data.error_code = washer_pb2.ERROR_AUTHCODE_EXPIRED
        common.send(socket, washer_pb2.REGISTER, pack_data)
        print 'authcode expired'
        return

    md5 = hashlib.md5()
    md5.update(password)
    password = md5.hexdigest()
    doc = {
        "nick": nick,        
        "phone": phone,
        "password": password,
        "avatar_small": avatar_small,
        "avatar_mid": avatar_mid,
        "avatar_big": avatar_big,
        "status": 0,
        "reg_time": now,
        "last_login": now,
        "level": base.WASHER_INIT_LEVEL
    }

    try:
        res = Washer.insert_one(doc)
        pack_data.washer.id = str(res.inserted_id)
        pack_data.error_code = washer_pb2.SUCCESS
        common.send(socket, washer_pb2.REGISTER, pack_data)
        print 'register success'
    except DuplicateKeyError:
        pack_data.error_code = washer_pb2.ERROR_WASHER_EXIST
        common.send(socket, washer_pb2.REGISTER, pack_data)
        print 'duplicate key error, member exist'

def verify_authcode(socket, data):
    unpack_data = washer_pb2.Verify_Authcode_Request()
    unpack_data.ParseFromString(data)
    
    phone = unpack_data.phone.strip()
    authcode = unpack_data.authcode
    signature = unpack_data.signature.strip()

    pack_data = washer_pb2.Verify_Authcode_Response()

    if not helper.verify_phone(phone):
        pack_data.error_code = washer_pb2.ERROR_PHONE_INVALID
        common.send(socket, washer_pb2.VERIFY_AUTHCODE, pack_data)
        print 'phone invalid'
        return
    
    filter = {
        "phone": phone,
        "authcode": authcode
    }
    washer_mix = Washer_Mix.find_one(filter)
    if washer_mix is None or washer_mix['authcode'] != authcode:
        pack_data.error_code = washer_pb2.ERROR_AUTHCODE_INVALID
        common.send(socket, washer_pb2.VERIFY_AUTHCODE, pack_data)
        print 'authcode invalid:%s' % (authcode)
        return
    elif washer_mix['expired'] < int(time.time()):
        pack_data.error_code = washer_pb2.ERROR_AUTHCODE_EXPIRED
        common.send(socket, washer_pb2.VERIFY_AUTHCODE, pack_data)
        print 'authcode expired'
        return

    pack_data.error_code = washer_pb2.SUCCESS
    common.send(socket, washer_pb2.VERIFY_AUTHCODE, pack_data)
    print 'verify authcode success'

def request_authcode(socket, data):
    unpack_data = washer_pb2.Request_Authcode_Request()
    unpack_data.ParseFromString(data)

    phone = unpack_data.phone.strip()
    signature = unpack_data.signature.strip()

    pack_data = washer_pb2.Request_Authcode_Response()

    if not helper.verify_phone(phone):
        pack_data.error_code = washer_pb2.ERROR_PHONE_INVALID
        common.send(socket, washer_pb2.REQUEST_AUTHCODE, pack_data)
        print 'phone invalid'
        return

    filter = {"phone":phone}
    washer_mix = Washer_Mix.find_one(filter)
    
    now = int(time.time())
    authcode = None
    if washer_mix is None:
        authcode = random.randint(base.AUTHCODE_MIN, base.AUTHCODE_MAX)
        expired  = now + base.AUTHCODE_EXPIRED_AFTER
        doc = {
            "phone": phone,
            "authcode": authcode,
            "expired": expired,
            "update_time": now
        }
        res = Washer_Mix.insert_one(doc)
        print 'create new authcode:%s' % (res)
    elif washer_mix['expired'] < now:
        authcode = random.randint(base.AUTHCODE_MIN, base.AUTHCODE_MAX)
        expired  = now + base.AUTHCODE_EXPIRED_AFTER
        doc = {
            "$set": {
                "authcode": authcode,
                "expired": expired,
                "update_time": now
            }
        }
        res = Washer_Mix.update_one(filter, doc)
        print 'update authcode:%s' % (res)

    authcode = authcode or washer_mix['authcode']
    pack_data.authcode = authcode
    pack_data.error_code = washer_pb2.SUCCESS
    print pack_data
    common.send(socket, washer_pb2.REQUEST_AUTHCODE, pack_data)
    #text =  "【趣游泳】您的验证码是是" + str(authcode)
    #response = helper.send_sms(text, phone[3:])

def fresh_location(socket, data):
    unpack_data = washer_pb2.Fresh_Location_Request()
    unpack_data.ParseFromString(data)

    city      = unpack_data.city.strip()
    longitude = unpack_data.longitude
    latitude  = unpack_data.latitude
   
    washer = get_online_washer_by_socket(socket)

    md5 = hashlib.md5() 
    md5.update(city)
    city = md5.hexdigest()

    pack_data = washer_pb2.Fresh_Location_Response()
    
    exploder = ' '
    cmd = ['GEOADD ']
    cmd.append(city)
    cmd.append(str(longitude))
    cmd.append(str(latitude))
    cmd.append(washer['phone'])
    cmd = exploder.join(cmd)
    
    try:
        common.redis.execute_command(cmd)
        pack_data.error_code = washer_pb2.SUCCESS
        common.send(socket, washer_pb2.FRESH_LOCATION_REQUEST, pack_data)
    except ResponseError as e:
        print e
        pack_data.error_code = washer_pb2.ERROR_FRESH_LOCATION_FAILURE
        common.send(socket, washer_pb2.FRESH_LOCATION_REQUEST, pack_data)
        return

def find_near_washer(city, longitude, latitude):
    explode = ' '
    cmd = ['GEORADIUS']
    cmd.append(city)
    cmd.append(str(longitude))
    cmd.append(str(latitude))
    cmd.append('3 km WITHCOORD')
    cmd = exploder.join(cmd)

    return common.redis.execute_command(cmd)
