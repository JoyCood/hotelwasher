#!/usr/bin/python 
# -*- coding: utf-8 -*-

import os
import sys
import socket
import inspect
import common

WASHER_PHONE = '+8618565389757'

def fresh_location(socket):
    pb = washer_pb2.Fresh_Location_Request()
    pb.phone = WASHER_PHONE
    pb.longitude = 21.1
    pb.latitude = 432.12
