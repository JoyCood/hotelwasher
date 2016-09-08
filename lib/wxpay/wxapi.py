#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import string
import hashlib
import random
import httplib
import xmltodict
from base import Base
from result import Result

class Wechat(Base):
    URL = "api.mch.weixin.qq.com";

    def __init__(self, appkey, appid, mchid):
        self.appkey = appkey
        self.values = dict()
        self.values['appid'] = appid
        self.values['mch_id'] = mchid

    def unified_order(self, out_trade_no, body, total_fee, notify_url):
	url = "api.mch.weixin.qq.com"
        self.values['out_trade_no'] = out_trade_no
        self.values['body'] = body
        self.values['total_fee'] = total_fee
        self.values['trade_type'] = 'APP'
        self.values['nonce_str'] = self.get_nonce_str()   
        self.values['notify_url'] = notify_url
        self.set_sign()
        xml = self.to_xml() 
        result = self.post_xml(xml, url)
        return Result(self.appkey, result).parse_xml()
        
    def order_query(self, **kwargs):
        if "out_trade_no" not in kwargs and "transaction_id" not in kwargs:
            raise
        if "out_trade_no" in kwargs:
            self.values['out_trade_no'] = kwargs['out_trade_no']
        else:
            self.values['transaction_id'] = kwargs['transaction_id']
        self.values['nonce_str'] = self.get_nonce_str()
        self.set_sign()
        xml = self.to_xml()
        result = self.post_xml(xml)
        return result

    def close_order(self, out_trade_no, timeout = 6):
        self.values['nonce_str'] = self.get_nonce_str()
        self.set_sign()
        xml = self.to_xml()
        result = self.post_xml(xml)

    def refund(self, out_refund_no, total_fee, refund_fee, op_user_id, out_trade_no=None, transaction_id=None):
        pass

    
if __name__=='__main__':
    appkey = 'f9c62cccbdc99de463304d89358788f9'
    appid  = 'wxd32d25b2a43c0f93'
    mchid  = '1312998901'

    out_trade_no = 5324313988
    body = 'product_title'
    total_fee = 100
    trade_type = 'APP' 
    notify_url = 'https://swim.7swim.com/swim/pay/weixin'

    api = Wechat(appkey, appid, mchid)
    api.unified_order(out_trade_no,body,total_fee,notify_url)
