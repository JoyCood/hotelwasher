from pymongo import MongoClient

import struct

mongo = MongoClient().hotelwasher

def send(socket, protocol, data):
    packet = data.SerializeToString()
    body_len = data.ByteSize()
    header = struct.pack('3I', body_len, protocol, 0)
    packet = header + packet
    socket.send(packet)
