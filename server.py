#!/usr/bin/python 
# -*- coding: utf-8 -*-

import sys, time, logging, struct, SocketServer
import daemon
from config import (mapper, base)
from importlib import import_module as loader

online_washer   = dict()
online_washer_socket_mapper = dict()
online_customer = dict()
online_guest    = dict()

class Request_Handler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.request.settimeout(base.SOCKET_RECEIVE_TIMEOUT)
        running = True
        while running:
            header = self.request.recv(base.SOCKET_HEADER_LENGTH)
            print repr(header)
            (body_len, api, protocol, num, sys) = struct.unpack('>5I', header)
            print("body_len:%s api:%s protocol:%s num:%s sys:%s") % (body_len, api, protocol, num, sys)
            h = struct.pack('>3I', 0, 1, 2)
            #(res_bodylen, res_protocol, res_num) = struct.unpack('>3I', h)
            #print("res_bodylen:%s res_protocol:%s res_num:%s") % (res_bodylen, res_protocol, res_num)
            #self.request.sendall(h)
            #return
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

def get_online_washer(phone):
    return online_washer.get(phone)

def get_online_washer_by_socket(socket):
    washer_phone = online_washer_socket_mapper.get(socket)
    return online_washer.get(washer_phone)

def add_online_washer(washer):
    online_washer[washer['phone']] = washer
    online_washer_socket_mapper[washer['socket']] = washer['phone']

def remove_online_washer(phone):
    try:
        washer = online_washer.get(phone)
        remove_online_washer_map(washer['socket'])
        del online_washer[phone]
    except KeyError:
        pass
    return True

def remove_online_washer_map(socket):
    try:
        del online_washer_socket_mapper[socket]
    except KeyError:
        pass
    return True

if __name__ == "__main__":
    __start_server__()
 
