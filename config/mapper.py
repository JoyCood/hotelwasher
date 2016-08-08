#!/usr/bin/python 
# -*- coding: utf-8 -*-

#模块映射
model = {
    '11':"member",
    '12':"order",
    "13":"washer"
}


#处理器
handler = {
    110000:"login", 
    110001:"request_authcode",
    110002:"verify_authcode",

    120000:"place_order",
    120001:"cancel_order",
    120002:"order_list",

    130000:"register",
    130001:"login",
    130002:"request_authcode",
    130003:"verify_authcode",
    130004:"fresh_location"
}
