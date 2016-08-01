#!/usr/bin/python 
# -*- coding: utf-8 -*-

#模块映射
model = {
    '11':"member",
    '12':"order"
}


#处理器
handler = {
    110000:"login", 
    110001:"register",
    110002:"request_authcode",
    110003:"verify_authcode",

    120000:"place_order",
    120001:"cancel_order",
    120002:"order_list"
}
