#!/usr/bin/python 
# -*- coding: utf-8 -*-

from model.member.main import member
from protocol.v1 import member_pb2
from config import (mapper, base)
from bson.objectid import ObjectId 

import phonenumbers

import sys
import hashlib
import random

def handle(socket, protocol, data):
    handler = mapper.handler.get(protocol)
    if handler == None:
        return
    fun = getattr(sys.modules[__name__], handler)
    fun(socket, data)

def login(socket, data):
    unpack_data = member_pb2.Login_Reqeust()
    unpack_data.ParseFromString(data)
    
    phone = unpack_data.phone.strip()
    password = unpack_data.password.strip()
    
def register(socket, data):
    unpack_data = member_pb2.Register_Request()
    unpack_data.ParseFromString(data)

    phone    = unpack_data.phone.strip();
    password = unpack_data.password.strip()
    authcode = unpack_data.authcode
    nick     = unpack_data.nick.strip()

def verify_authcode(socket, data):
    unpack_data = member_pb2.Verify_Phone_Request()
    unpack_data = unpack_data.ParseFromString(data)

    phone    = unpack_data.phone.strip()
    authcode = unpack_data.authcode
    
    phone_number = phonenumbers.parse(phone, "CN")
    pack_data = member_pb2.Register_Response()

    if not phonenumbers.is_valid_number(phone_number):
        pack_data.code = member_pb2.ERROR_PHONE_INVALID
        common.send(socket, pack_data)
        return
    
    filter = {
        "phone": phone,
        "authcode" : authcode
    }
    member_mix = Member_Mix.find_one(filter)
    if member_mix is None or member_mix['authcode'] != authcode:
        pack_data.code = member_pb2.ERROR_AUTHCODE_INVALID
        common.send(socket, pack_data)
        return
    elif attach['expired'] < int(time.time()):
        pack_data.code = member_pb2.ERROR_AUTHCODE_EXPIRED
        common.send(socket, pack_data)
        return
    pack_data.code = member_pb2.ERROR_SUCCESS
    common.send(socket, pack_data)

def request_authcode(socket, data):
    unpack_data = member_pb2.Request_Authcode_Request()
    unpack_data.ParseFromString(data)

    phone = unpack_data.phone.strip()
    
    phone_number = phonenumbers.parse(phone, "CN")
    pack_data = member_pb2.Request_Authcode_Response()

    if not phonenumbers.is_valid_number(phone_number):
        pack_data.code = member_pb2.ERROR_PHONE_INVALID
        common.send(socket, pack_data)
        return
    filter = {"phone":phone}

    member_mix = Member_Mix.find_one(filter)
    
    now = int(time.time())

    if member_mix is None:
        authcode = random.randint(base.AUTHCODE_MIN, base.AUTHCODE_MAX)
        expired  = now + base.AUTHCODE_EXPIRED_AFTER
        doc = {
            "phone": phone,
            "authcode": authcode,
            "expired": expired,
            "update_time": now
        }
        Member_Mix.insert_one(doc)
    elif member_mix['expired'] < now:
        authcode = random.randint()
        expired  = now + base.AUTHCODE_EXPIRED_AFTER
        doc = {
            "$set": {
                "authcode": authcode,
                "expired": expired,
                "update_time": now
            }        
        }
        Member_Mix.update_one(filter, doc)
    pack_data.code = member_pb2.ERROR_SUCCESS
    pack_data.authcode = authcode
    common.send(socket, pack_data)

