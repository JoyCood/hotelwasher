#!/usr/bin/python 
# -*- coding: utf-8 -*-
import os
import sys
import socket 
import struct 
import inspect
import json

def fun_filter(fun):
    name, value = fun
    return name

def send(socket, protocol, data):
    packet = data.SerializeToString()
    body_len = data.ByteSize()
    header = struct.pack('5I', body_len, 1, protocol, 0, 1)
    packet = header + packet
    res = socket.send(packet)

def request_authcode(socket):
    member = member_pb2.Request_Authcode_Request()
    member.phone = "+8618565389757"
    send(socket,110003, member)
    print 'request_authcode'

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
