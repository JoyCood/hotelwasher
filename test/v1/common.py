#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import socket
import struct
import inspect

def fun_filter(fun):
    name, value = fun
    return name

def send(socket, protocol, data):
    packet = data.SerializeToString()
    body_len = data.ByteSize()
    header = struct.pack('>5I', body_len, 1, protocol, 0, 1)
    packet = header + packet
    return socket.send(packet)

def get(socket):
    header = socket.recv(12)
    if header:
        (body_len, protocol, num) = struct.unpack('>3I', header)
        if body_len:
            body = socket.recv(body_len)
            return body
    return False


