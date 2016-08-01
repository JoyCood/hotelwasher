#!/usr/bin/python 
# -*- coding: utf-8 -*-

from model.member.main import Member
from model.member.mix  import Member_Mix
from protocol.v1 import member_pb2
from config import (mapper, base)
from helper import helper
from bson.objectid import ObjectId 
from pymongo.errors import DuplicateKeyError

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

def login(socket, data):
    unpack_data = member_pb2.Login_Reqeust()
    unpack_data.ParseFromString(data)
    
    phone = unpack_data.phone.strip()
    password = unpack_data.password.strip()

    pack_data = member_pb2.Login_Response()
    md5 = hashlib.md5()
    md5.update(password)
    password = md5.hexdigest()

    phone_number = phonenumbers.parse(phone, "CN")

    if not phonenumbers.is_valid_number(phone_number):
        pack_data.error_code = member_pb2.ERROR_PHONE_INVALID
        common.send(socket, member_pb2.LOGIN, pack_data)
        print 'phone invalid'
        return

    filter = {
        "phone": phone
    }
    member = Member.find_one(filter)
    if member is None:
        pack_data.error_code = member_pb2.ERROR_MEMBER_NOT_FOUND
        common.send(socket, member_pb2.LOGIN, pack_data)
        print 'member not found'
        return
    elif member['password'] != password:
        pack_data.error_code = member_pb2.ERROR_PASSWORD_INVALID
        common.send(socket, member_pb2.LOGIN, pack_data)
        print 'password invalid'
        return
    pack_data.member.id = str(member['_id'])
    pack_data.member.nick = member['nick']
    pack_data.error_code = member_pb2.SUCCESS
    common.send(socket, member_pb2.LOGIN, pack_data)
    print 'login success'

def register(socket, data):
    unpack_data = member_pb2.Register_Request()
    unpack_data.ParseFromString(data)

    nick     = unpack_data.nick.strip()
    phone    = unpack_data.phone.strip();
    password = unpack_data.password.strip()
    confirm_password = unpack_data.confirm_password.strip()
    authcode = unpack_data.authcode

    phone_number = phonenumbers.parse(phone, "CN")

    pack_data = member_pb2.Register_Response()
    
    if password != confirm_password:
        pack_data.error_code = member_pb2.ERROR_PASSWORD_NOT_EQUAL
        common.send(socket, member_pb2.REGISTER, pack_data)
        print 'password not equal'
        return
    elif not phonenumbers.is_valid_number(phone_number):
        pack_data.error_code = member_pb2.ERROR_PHONE_INVALID
        common.send(socket, member_pb2.REGISTER, pack_data)
        print 'phone invalid'
        return

    now    = int(time.time()) 
    filter = {"phone":phone}
    member = Member.find_one(filter);
    
    if member is not None:
        pack_data.error_code = member_pb2.ERROR_MEMBER_EXIST
        common.send(socket, member_pb2.REGISTER, pack_data)
        print 'member exist'
        return

    member_mix = Member_Mix.find_one(filter)

    if member_mix is None or member_mix['authcode'] != authcode:
        pack_data.error_code = member_pb2.ERROR_AUTHCODE_INVALID
        common.send(socket,member_pb2.REGISTER, pack_data)
        print 'authcode invalid'
        return
    elif member_mix['expired'] < now:
        pack_data.error_code = member_pb2.ERROR_AUTHCODE_EXPIRED
        common.send(socket, member_pb2.REGISTER, pack_data)
        print 'authcode expired'
        return
    md5 = hashlib.md5()
    md5.update(password)
    password = md5.hexdigest()
    doc = {
        "nick": nick,
        "phone": phone,
        "password": password,
        "status": 0,
        "reg_time": now,
        "last_login": now
    }
    try:
        res = Member.insert_one(doc)
        pack_data.member.id = str(res.inserted_id)
        pack_data.error_code = member_pb2.SUCCESS
        common.send(socket, member_pb2.REGISTER, pack_data)
        print 'register success'
    except DuplicateKeyError:
        pack_data.error_code = member_pb2.ERROR_MEMBER_EXIST
        common.send(socket, member_pb2.REGISTER, pack_data)
        print 'duplicate key error, member exist'


def verify_authcode(socket, data):
    unpack_data = member_pb2.Verify_Authcode_Request()
    unpack_data.ParseFromString(data)
    phone = unpack_data.phone.strip()
    authcode = unpack_data.authcode
    
    phone_number = phonenumbers.parse(phone, "CN")
    pack_data = member_pb2.Verify_Authcode_Response()

    if not phonenumbers.is_valid_number(phone_number):
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

def request_authcode(socket, data):
    unpack_data = member_pb2.Request_Authcode_Request()
    unpack_data.ParseFromString(data)

    phone = unpack_data.phone.strip()
    
    phone_number = phonenumbers.parse(phone, "CN")
    pack_data = member_pb2.Request_Authcode_Response()

    if not phonenumbers.is_valid_number(phone_number):
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
    pack_data.error_code = member_pb2.SUCCESS
    pack_data.authcode = authcode

    common.send(socket,member_pb2.REQUEST_AUTHCODE, pack_data)
    text = "【趣游泳】您的验证码是是" + str(authcode)  
    response = helper.send_sms(text, phone[3:])
    print 'request authcode response:%s' % (response)

