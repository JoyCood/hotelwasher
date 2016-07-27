#!/usr/bin/python 
# -*- coding: utf-8 -*-

import sys, time, logging, struct, SocketServer
import daemon
from config import (mapper, base)
from importlib import import_module as loader

class Reqeust_Handler(SocketServer.BaseReqeustHandler):
    def handle(self):
        self.request.settimeout(base.SOCKET_RECEIVE_TIMEOUT)
        running = True
        while running:
            try:
                header = self.request.recv(base.SOCKET_HEADER_LENGTH)
                (body_len, api, protocol, num, sys) = struct.unpack('5I', header)
                body = self.request.recv(body_len)
                __router__(self.request, api, protocol, body)
            except Exception as e:
                running = False
                self.request.close()

class Server(SocketServer.ThreadingmixIn, SocketServer.TCPServer):
    def verify_request(self, request, client_address):
        print 'verify_request called...'
        return True


def __router__(socket, api, protocol, data):
    """ 分发到对应的业务模块处理业务 """
    api = 'api.v' + str(api)
    index = str(protocol)[:2]
    model = mapper.model.get(index) #根据协议前两位获取对应模块
    if model is None: #找不到对应模块
        return
    model = loader('.'+model, api)
    model.handle(socket, protocol, data)

def __start_server__():
    #with daemon.DaemonContext():
        server = Server((base.SERVER_HOST, base.SERVER_PORT), Request_Handler)
        server.server_forever()

def stop_server():
    pass

def restart():
    stop_server()
    start_server()

if __name__ == "__main__":
    start_server()
