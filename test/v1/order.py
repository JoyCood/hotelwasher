#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import socket
import struct
import inspect
import common
import hashlib

def place_order(socket):
    pb = order_pb2.Place_Order_Request()
    pb.city_code = 179
    pb.type = order_pb2.NORMAL
    pb.quantity = 2
    pb.longitude = 120.21937542
    pb.latitude = 30.25924446
    common.send(socket, order_pb2.PLACE_ORDER, pb)
    body = common.get(socket)
    
    res = order_pb2.Place_Order_Response()
    res.ParseFromString(body)
    print res

if __name__ == '__main__':
    filepath = os.path.realpath(__file__)
    name = os.path.dirname(os.path.realpath(__file__))[:-8]
    print name
    sys.path.append(os.path.dirname(os.path.realpath(__file__))[:-8])
    from config import base
    from protocol.v1 import order_pb2
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((base.SERVER_HOST, base.SERVER_PORT))

    sys.stdout.write("%")

    while True:
        fun = sys.stdin.readline()
        if fun == 'quit':
            client.close()
            break
        fun = fun.strip('\n')
        fun_list = inspect.getmembers(sys.modules[__name__], inspect.isfunction)
        fun_list = map(common.fun_filter, fun_list)
        if fun in fun_list:
            f = getattr(sys.modules[__name__], fun)
            f(client)
