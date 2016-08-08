#!/usr/bin/python 
# -*- coding: utf-8 -*-

from model.member.main import Member
from model.member.mix  import Member_Mix
from protocol.v1 import member_pb2
from config import (mapper, base)
from helper import helper
from bson.objectid import ObjectId 
from pymongo.errors import DuplicateKeyError
from server import (
        get_online_customer_by_phone,
        add_online_customer,
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

def order_check(socket, data):
    unpack_data = member_pb2.Login_Reqeust()
    unpack_data.ParseFromString(data)
    
    phone     = unpack_data.phone.strip()
    uuid      = unpack_data.uuid.strip()
    signature = unpack_data.signature.strip()
    
    if not helper.verify_phone(phone):
        pack_data.error_code = member_pb2.ERROR_PHONE_INVALID
        common.send(socket, member_pb2.LOGIN, pack_data)
        return

    filter = {"phone":phone}
    member_mix = Member_Mix.find_one(filter)
    if member_mix is None:
        pack_data.error_code = member_pb2.ERROR_SIGNATURE_INVALID
        common.send(socket, member_pb2.LOGIN, pack_data)
        return
    
    signature2 = [member_mix['secret']]
    signature2.append(phone)
    signature2.append(uuid)
    signature2 = exploder.join(signature2)

    md5 = hashlib.md5()
    md5.update(signature2)
    signature2 = md5.hexdigest()

    if signature2 != signature:
        pack_data.error_code = member_pb2.ERROR_SIGNATURE_INVALID
        common.send(socket, member_pb2.LOGIN, pack_data)
        return
    

            
#踢出其它已登录帐号
def __kickout__(phone,socket):
    customer = get_online_customer_by_phone(phone)
    if customer and customer['socket'] != socket:
        print 'customer socket:%s socket2:%s' % (customer['socket'], socket)
        pack_data = member_pb2.Login_Response()
        pack_data.error_code = member_pb2.ERROR_KICKOUT
        common.send(customer['socket'], member_pb2.KICKOUT, pack_data)
        customer['socket'].close()

#登录
def login(socket, data):
    unpack_data = member_pb2.Login_Request()
    unpack_data.ParseFromString(data)

    phone    = unpack_data.phone.strip();
    authcode = unpack_data.authcode
    uuid     = unpack_data.uuid

    pack_data = member_pb2.Login_Response()
    
    if not helper.verify_phone(phone):
        pack_data.error_code = member_pb2.ERROR_PHONE_INVALID
        common.send(socket, member_pb2.LOGIN, pack_data)
        print 'phone invalid'
        return

    now    = int(time.time()) 
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
    
    secret = str(time.time()) +  base.APPKEY + phone + helper.get_random(6) + uuid
    md5 = hashlib.md5()
    md5.update(secret)
    secret = md5.hexdigest()

    filter = {"phone":phone}
    
    doc = {"$set":{"secret":secret}} 

    Member_Mix.update_one(filter, doc)
    pack_data.phone  = phone
    pack_data.secret = secret
    pack_data.uuid   = uuid 
    pack_data.error_code = member_pb2.SUCCESS
    common.send(socket, member_pb2.LOGIN, pack_data)

#验证码校验
def verify_authcode(socket, data):
    unpack_data = member_pb2.Verify_Authcode_Request()
    unpack_data.ParseFromString(data)
    phone = unpack_data.phone.strip()
    authcode = unpack_data.authcode
    
    pack_data = member_pb2.Verify_Authcode_Response()

    if not helper.verify_phone(phone):
        pack_data.error_code = member_pb2.ERROR_PHONE_INVALID
        common.send(socket, member_pb2.VERIFY_AUTHCODE, pack_data)
        return
    
    filter = {
        "phone": phone,
        "authcode" : authcode
    }
    member_mix = Member_Mix.find_one(filter)
    if member_mix is None or member_mix['authcode'] != authcode:
        pack_data.error_code = member_pb2.ERROR_AUTHCODE_INVALID
        common.send(socket, member_pb2.VERIFY_AUTHCODE, pack_data)
        print 'authcode invalid:%s' % (authcode)
        return
    elif member_mix['expired'] < int(time.time()):
        pack_data.error_code = member_pb2.ERROR_AUTHCODE_EXPIRED
        common.send(socket, member_pb2.VERIFY_AUTHCODE, pack_data)
        print 'authcode expired'
        return
    pack_data.error_code = member_pb2.SUCCESS
    common.send(socket, member_pb2.VERIFY_AUTHCODE, pack_data)
    print 'verify authcode success'

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

def get_secret(phone):
    member = server.get_online_customer_by_phone(phone)
    if member is None:
        filter = {"phone":phone}
        member_mix = Member_Mix.find_one(filter)
        return member_mix.get('secret')
    return member.get('secret')
