#!/usr/bin/python 
# -*- coding: utf-8 -*-
import os
import sys
import socket 
import struct 
import inspect
import common
import hashlib

TEST_PHONE = '+8613533332421'

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

def request_authcode(socket):
    member = member_pb2.Request_Authcode_Request()
    member.phone = TEST_PHONE
    common.send(socket,member_pb2.REQUEST_AUTHCODE, member)
    body = common.get(socket)
    if body:
        pb = member_pb2.Request_Authcode_Response()
        pb.ParseFromString(body)
        verify_authcode(socket, pb.authcode)
        login(socket, pb.authcode)

def verify_authcode(socket, authcode):
    pb = member_pb2.Verify_Authcode_Request()
    pb.phone = TEST_PHONE
    pb.authcode = authcode

    common.send(socket, member_pb2.VERIFY_AUTHCODE, pb)
    body = common.get(socket)
    if body:
        unpack_data = member_pb2.Verify_Authcode_Response()
        unpack_data.ParseFromString(body)
        print 'verify_authcode:%s' % (unpack_data.error_code)

if __name__ == '__main__':
    filepath = os.path.realpath(__file__)
    sys.path.append(os.path.dirname(os.path.realpath(__file__))[:-8])
    from config import base
    from protocol.v1 import member_pb2

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
