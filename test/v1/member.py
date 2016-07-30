#!/usr/bin/python 
# -*- coding: utf-8 -*-
import os
import sys
import socket 
import struct 
import inspect
import json

TEST_PHONE = '+8613533332421'

def fun_filter(fun):
    name, value = fun
    return name

def send(socket, protocol, data):
    packet = data.SerializeToString()
    body_len = data.ByteSize()
    header = struct.pack('5I', body_len, 1, protocol, 0, 1)
    packet = header + packet
    return socket.send(packet)


def rec(socket):
    header = socket.recv(12)
    if header:
        (body_len, protocol, num) = struct.unpack('3I', header)
        if body_len:
            body = socket.recv(body_len)
            return body
        else:
            return False
    else:
        return False

def login(socket):
    pb = member_pb2.Login_Reqeust()
    pb.phone = TEST_PHONE
    pb.password = 'iwasher'
    send(socket, member_pb2.LOGIN, pb)
    body = rec(socket)
    if body:
        pb = member_pb2.Login_Response()
        pb.ParseFromString(body)
        print pb

def register(socket, authcode):
    pb = member_pb2.Register_Request()
    pb.phone = TEST_PHONE
    pb.password = 'iwasher'
    pb.confirm_password = 'iwasher'
    pb.authcode = authcode
    pb.nick = 'iwahser'
    send(socket, member_pb2.REGISTER, pb)
    body = rec(socket)
    if body:
        pb = member_pb2.Register_Response()
        pb.ParseFromString(body)
        print pb

def request_authcode(socket):
    member = member_pb2.Request_Authcode_Request()
    member.phone = TEST_PHONE
    send(socket,member_pb2.REQUEST_AUTHCODE, member)
    body = rec(socket)
    if body:
        pb = member_pb2.Request_Authcode_Response()
        pb.ParseFromString(body)
        verify_authcode(socket, pb.authcode)

def verify_authcode(socket, authcode):
    pb = member_pb2.Verify_Authcode_Request()
    pb.phone = TEST_PHONE
    pb.authcode = authcode

    send(socket, member_pb2.VERIFY_AUTHCODE, pb)
    body = rec(socket)
    if body:
        unpack_data = member_pb2.Verify_Authcode_Response()
        unpack_data.ParseFromString(body)
        register(socket, 4651)
        print 'verify_authcode:%s' % (unpack_data.error_code)

if __name__ == '__main__':
    filepath = os.path.realpath(__file__)
    sys.path.append(os.path.dirname(os.path.realpath(__file__))[:-8])
    from config import base
    from protocol.v1 import member_pb2
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((base.SERVER_HOST, base.SERVER_PORT))
    sys.stdout.write("%")

    while True:
        fun = sys.stdin.readline()
        if fun == '\n':
            client.close()
            break
        fun2 = fun.strip('\n')
        fun_list = inspect.getmembers(sys.modules[__name__], inspect.isfunction)
        fun_list = map(fun_filter, fun_list)
        if fun2 in fun_list:
            f = getattr(sys.modules[__name__], fun2)
            f(client)
