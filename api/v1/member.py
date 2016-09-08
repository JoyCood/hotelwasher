#!/usr/bin/python 
# -*- coding: utf-8 -*-

from model.member.mix  import Member_Mix
from model.order.main import Order
from protocol.v1 import (
        member_pb2, 
        order_pb2,
        washer_pb2)
from config import (mapper, base)
from helper import helper
from bson.objectid import ObjectId 
from pymongo.errors import DuplicateKeyError
from server import (
        get_online_customer_by_phone,
        get_online_customer_by_socket,
        add_online_customer,
        get_online_washer_by_phone
)

import common
import phonenumbers

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
    
#踢出其它已登录帐号
def __kickout__(phone,socket):
    customer = get_online_customer_by_phone(phone)
    if customer and customer['socket'] != socket:
        print 'customer socket:%s socket2:%s' % (customer['socket'], socket)
        pack_data = member_pb2.Login_Response()
        pack_data.error_code = member_pb2.SUCCESS
        common.send(customer['socket'], member_pb2.KICKOUT, pack_data)
        customer['socket'].close()

#登录
def login(socket, data):
    unpack_data = member_pb2.Login_Request()
    unpack_data.ParseFromString(data)

    phone     = unpack_data.phone.strip();
    authcode  = unpack_data.authcode
    uuid      = unpack_data.uuid
    signature = unpack_data.signature.strip()

    pack_data = member_pb2.Login_Response()
    
    if not helper.verify_phone(phone):
        pack_data.error_code = member_pb2.ERROR_PHONE_INVALID
        common.send(socket, member_pb2.LOGIN, pack_data)
        print 'phone invalid'
        return
    if authcode:
        __login__(socket, phone, authcode, uuid)
        return
    __reconnect__(socket, phone, uuid, signature)

#重连
def __reconnect__(socket, phone, uuid, signature):
    pack_data =  member_pb2.Login_Response()

    valid = verify_signature(phone, uuid, signature)
    if not valid:
        pack_data.error_code = member_pb2.ERROR_SIGNATURE_INVALID
        common.send(socket, member_pb2.LOGIN, pack_data)
        return

    __kickout__(phone, socket)
    
    filter = {"phone":phone}
    member_mix = Member_Mix.find_one(filter)

    customer = {
        "id": str(member_mix['_id']),
        "phone": member_mix['phone'],
        "socket": socket
    }

    add_online_customer(customer)

    pack_data.phone = phone
    pack_data.uuid  = uuid
    pack_data.secret = member_mix['secret']
    pack_data.error_code = member_pb2.SUCCESS
    common.send(socket, member_pb2.LOGIN, pack_data)
    sync_order(socket)

#同步未完成的订单
def sync_order(socket):
    customer = get_online_customer_by_socket(socket)
    filter = {"customer_phone":customer['phone'], "feedback":0}
         
    order = Order.find_one(filter)

    pack_data = order_pb2.Customer_Processing_Order_Response()

    if order is None:
        pack_data.error_code = order_pb2.SUCCESS
        common.send(socket, order_pb2.CUSTOMER_PROCESSING_ORDER, pack_data)
        return
    
    washer = get_online_washer_by_phone(order['washer_phone'])
    
    if washer is None:
        filter = {"phone":order['washer_phone']}
        washer = Washer.find_one(filter)
        if washer is not None:
            washer['id'] = str(washer['_id'])
            del washer['_id']

    pack_data.order_id     = str(order['_id'])
    pack_data.quantity     = order['quantity']
    pack_data.price        = order['price']
    pack_data.order_type   = order['order_type']
    pack_data.washer.id    = washer['id']
    pack_data.washer.phone = washer['phone']
    pack_data.washer.nick  = washer['nick']
    pack_data.washer.level = washer['level']
    pack_data.error_code = order_pb2.SUCCESS

    print 'get not finish order:'
    print pack_data
    common.send(socket, order_pb2.SYNC_ORDER, pack_data)

#通过验证码登录
def __login__(socket, phone, authcode, uuid):
    pack_data = member_pb2.Login_Response()

    now = int(time.time()) 
    
    filter = {"phone":phone}
    member_mix = Member_Mix.find_one(filter);
    
    if member_mix is None:
        pack_data.error_code = member_pb2.ERROR_AUTHCODE_INVALID
        common.send(socket, member_pb2.LOGIN, pack_data)
        return

    if member_mix['authcode'] != authcode:
        pack_data.error_code = member_pb2.ERROR_AUTHCODE_INVALID
        common.send(socket, member_pb2.LOGIN, pack_data)
        print 'authcode invalid'
        return

    if member_mix['expired'] < now:
        pack_data.error_code = member_pb2.ERROR_AUTHCODE_EXPIRED
        common.send(socket, member_pb2.LOGIN, pack_data)
        print 'authcode expired'
        return

    __kickout__(phone, socket)

    secret = make_secret(phone, uuid)    

    customer = {
        "id": str(member_mix['_id']),
        "phone": member_mix['phone'],
        "socket": socket
    }

    add_online_customer(customer)
   
    pack_data.phone  = phone
    pack_data.secret = secret
    pack_data.uuid   = uuid 
    pack_data.error_code = member_pb2.SUCCESS
    common.send(socket, member_pb2.LOGIN, pack_data)
    sync_order(socket)
 
#请求验证码
def request_authcode(socket, data):
    unpack_data = member_pb2.Request_Authcode_Request()
    unpack_data.ParseFromString(data)

    phone = unpack_data.phone.strip()
    
    pack_data = member_pb2.Request_Authcode_Response()

    if not helper.verify_phone(phone):
        pack_data.error_code = member_pb2.ERROR_PHONE_INVALID
        common.send(socket, member_pb2.REQUEST_AUTHCODE, pack_data)
        print 'phone invalid'
        return
    filter = {"phone":phone}

    member_mix = Member_Mix.find_one(filter)
    
    now = int(time.time())
    authcode = None
    if member_mix is None:
        authcode = random.randint(base.AUTHCODE_MIN, base.AUTHCODE_MAX)
        expired  = now + base.AUTHCODE_EXPIRED_AFTER
        doc = {
            "phone": phone,
            "authcode": authcode,
            "expired": expired,
            "update_time": now
        }
        res = Member_Mix.insert_one(doc)
        print 'create new authcode:%s' % (res)
    elif member_mix['expired'] < now:
        authcode = random.randint(base.AUTHCODE_MIN, base.AUTHCODE_MAX)
        expired  = now + base.AUTHCODE_EXPIRED_AFTER
        doc = {
            "$set": {
                "authcode": authcode,
                "expired": expired,
                "update_time": now
            }        
        }
        res = Member_Mix.update_one(filter, doc)
        print 'update authcode:%s' % (res)

    authcode = authcode or member_mix['authcode']

    pack_data.authcode   = authcode
    pack_data.error_code = member_pb2.SUCCESS

    common.send(socket,member_pb2.REQUEST_AUTHCODE, pack_data)
    text = "【趣游泳】您的验证码是是" + str(authcode)  
    response = helper.send_sms(text, phone[3:])
    print 'request authcode response:%s' % (response)

#生成令牌
def make_secret(phone, uuid):
    now = time.time()
    elements = [str(now)]
    elements.append(base.APPKEY)
    elements.append(uuid)
    elements.append(helper.get_random(6))
    elements.append(phone)
    secret = ''.join(elements)
    md5 = hashlib.md5()
    md5.update(secret)
    secret = md5.hexdigest()
    filter = {"phone": phone}
    update = {"$set":{"secret":secret}}
    Member_Mix.update_one(filter, update)
    return secret

#校验签名
def verify_signature(phone, uuid, signature):
    filter = {"phone":phone}
    customer = Member_Mix.find_one(filter)
    if customer is None:
        return False
    signature2 = [customer['secret']]
    signature2.append(base.APPKEY)
    signature2.append(uuid)
    signature2.append(phone)

    signature2 = ''.join(signature2)
    md5 = hashlib.md5()
    md5.update(signature2)
    signature2 = md5.hexdigest()

    return signature2 == signature

#查找附近的商家
def find_near_washer(socket, data):
    unpack_data = member_pb2.Near_Washer_Request()
    unpack_data.ParseFromString(data)
    
    city_code = unpack_data.city_code
    longitude = unpack_data.longitude
    latitude  = unpack_data.latitude

    exploder = ' '

    cmd = ['GEORADIUS']
    cmd.append(str(city_code))
    cmd.append(str(longitude))
    cmd.append(str(latitude))
    cmd.append('3 km WITHDIST WITHCOORD') #3km内的商家
    cmd = exploder.join(cmd)
    
    pack_data = member_pb2.Near_Washer_Response()

    washers = common.redis.execute_command(cmd)

    for item in washers:
        phone     = item[0]
        distance  = item[1]
        longitude = item[2][0]
        latitude  = item[2][1]

        washer = get_online_washer_by_phone(phone)

        if washer is None:
            filter = {"phone":phone}
            washer = Washer.find_one(filter)
            if washer is None:
                continue
            washer['id'] = str(washer['_id'])
            del washer['_id']

        washer_tmp = pack_data.washer.add()
        washer_tmp.id = washer['id']
        washer_tmp.nick = washer['nick']
        washer_tmp.phone = washer['phone']
        washer_tmp.avatar_small = washer['avatar_small']
        washer_tmp.level = washer['level']
        washer_tmp.longitude = float(longitude)
        washer_tmp.latitude = float(latitude)
    
    pack_data.error_code = washer_pb2.SUCCESS
    common.send(socket, member_pb2.NEAR_WASHER, pack_data)
