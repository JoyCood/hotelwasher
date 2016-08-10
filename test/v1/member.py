#!/usr/bin/python 
# -*- coding: utf-8 -*-
import os
import sys
import socket 
import struct 
import inspect
import common
import hashlib

TEST_PHONE = '+8618565389757'

def login(socket, authcode):
    pb = member_pb2.Login_Request()
    pb.phone = TEST_PHONE
    pb.authcode = authcode
    pb.uuid = 'abcdefg'
    common.send(socket, member_pb2.LOGIN, pb)
    while True:
        body = common.get(socket)
        if body:
            pb = member_pb2.Login_Response()
            pb.ParseFromString(body)
        
            if pb.error_code == member_pb2.ERROR_KICKOUT:
                print 'kickout!'
                break

            print 'login success:'
            print pb
        else:
            print 'body is empty!'
            socket.close()
            break

def reconnect(socket):
    secret = 'b42aa8660f6e30362c85f6bb9a18f068'
    pb = member_pb2.Login_Request()
    uuid = 'abcdefg'
    signature = secret + base.APPKEY + uuid + TEST_PHONE
    md5 = hashlib.md5()
    md5.update(signature)
    signature = md5.hexdigest()
    
    pb.phone = TEST_PHONE
    pb.uuid  = uuid
    pb.signature = signature
    common.send(socket, member_pb2.LOGIN, pb)
    while True:
        body = common.get(socket)
        if body:
            pb = member_pb2.Login_Response()
            pb.ParseFromString(body)
            print pb

def request_authcode(socket):
    member = member_pb2.Request_Authcode_Request()
    member.phone = TEST_PHONE
    common.send(socket,member_pb2.REQUEST_AUTHCODE, member)
    body = common.get(socket)
    if body:
        pb = member_pb2.Request_Authcode_Response()
        pb.ParseFromString(body)
        login(socket, pb.authcode)

if __name__ == '__main__':
    filepath = os.path.realpath(__file__)
    sys.path.append(os.path.dirname(os.path.realpath(__file__))[:-8])
    from config import base
    from protocol.v1 import member_pb2
    from protocol.v1 import order_pb2

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((base.SERVER_HOST, base.SERVER_PORT))
    sys.stdout.write("%")
    
    client.settimeout(20)
    while True:
        fun = sys.stdin.readline()
        if fun == '\n':
            client.close()
            break
        fun2 = fun.strip('\n')
        fun_list = inspect.getmembers(sys.modules[__name__], inspect.isfunction)
        fun_list = map(common.fun_filter, fun_list)
        if fun2 in fun_list:
            f = getattr(sys.modules[__name__], fun2)
            f(client)
