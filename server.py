#!/usr/bin/python 
# -*- coding: utf-8 -*-

import sys, time, logging, struct, SocketServer
import daemon
import socket
from config import (mapper, base)
from importlib import import_module as loader


online_washer = dict()
online_washer_mapper = dict()
online_customer = dict()
online_customer_mapper = dict()

class Request_Handler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.request.settimeout(base.SOCKET_RECEIVE_TIMEOUT)
        running = True
        while running:
            try:
                header = self.request.recv(base.SOCKET_HEADER_LENGTH)
            except socket.error as e:
                print 'close the socket'
                self.request.close()
                running = False
            else:
                print repr(header)
                (body_len, api, protocol, num, sys) = struct.unpack('>5I', header)
                print("body_len:%s api:%s protocol:%s num:%s sys:%s") % (body_len, api, protocol, num, sys)
                body = self.request.recv(body_len)
                __router__(self.request, api, protocol, body)

class Server(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def verify_request(self, request, client_address):
        print 'verify_request called...'
        return True


def __router__(socket, api, protocol, data):
    """ 分发到对应的业务模块处理业务 """
    api = 'api.v' + str(api)
    index = str(protocol)[:2]
    print mapper.model
    model = mapper.model.get(index) #根据协议前两位获取对应模块

    print 'model prefix:%s, model:%s' % (index, model)
    if model is None: #找不到对应模块
        print 'model not found'
        return
    model = loader('.'+model, api)
    model.handle(socket, protocol, data)

def __start_server__():
    #with daemon.DaemonContext():
        server = Server((base.SERVER_HOST, base.SERVER_PORT), Request_Handler)
        server.serve_forever()

def stop_server():
    pass

def restart():
    stop_server()
    start_server()

def add_online_washer(washer):
    online_washer[washer['phone']] = washer
    online_washer_mapper[washer['socket']] = washer['phone']

def get_online_washer_by_phone(phone):
    return online_washer.get(phone)

def get_online_washer_by_socket(socket):
    washer_phone = online_washer_mapper.get(socket)
    return online_washer.get(washer_phone)

def remove_online_washer_by_phone(phone):
    try:
        washer = online_washer.get(phone)
        del online_washer[phone]
        del online_washer_mapper[washer['socket']]
    except (TypeError, KeyError):
        pass
    return True

def remove_online_washer_by_socket(socket):
    try:
        washer = get_online_washer_by_socket(socket)
        del online_washer[washer['phone']]
        del online_washer_mapper[socket]
    except (TypeError, KeyError):
        pass
    return True
#--------------------------------------------
def add_online_customer(member):
    online_customer[member['phone']] = member
    online_customer_mapper[member['socket']] = member['phone']

def remove_online_customer_by_phone(phone):
    try:
        member = online_customer.get(phone)
        del online_customer[member['phone']]
        del online_washer_mapper[member['socket']]
    except (TypeError, KeyError):
        pass

def remove_online_customer_by_socket(socket):
    try:
        customer = get_online_customer_by_socket(socket)
        del online_customer[customer['phone']]
        del online_customer_mapper[socket]
    except (TypeError, KeyError):
        pass
    return True

def get_online_customer_by_phone(phone):
    return online_customer.get(phone)

def get_online_customer_by_socket(socket):
    member_phone = online_customer_mapper.get(socket)
    return online_customer.get(member_phone)

if __name__ == "__main__":
    __start_server__()
 
