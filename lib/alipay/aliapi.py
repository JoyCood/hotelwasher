#!/usr/bin/python
# -*- coding: utf-8 -*-

from OpenSSL import crypto
import base64

class Alipay(object):
    def __init__(self, alipay_config):
        self.alipay_config = alipay_config
    
    #global function
    def para_filter(self, param):
        paramters = dict()
        ignore = ['sign_type']
        for key, value in param.items():
            if key in ignore or value=='':
                continue
            paramters[key] = value
        return paramters

    #global function
    def create_link_string(self, param):
        paramters = list()
        for key, value in param.items():
            paramters.append(key)
            paramters.append('="')
            paramters.append(str(value))
            paramters.append('"&')
        paramters = ''.join(paramters)
        return paramters.strip('&')

    def rsa_sign(self, data, private_key_path):
        private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, open(private_key_path).read())
        sign = crypto.sign(private_key, data, 'sha1')
        return base64.b64encode(sign)

    def build_request_sign(self, param):
        paramters = self.create_link_string(param)
        return self.rsa_sign(paramters, self.alipay_config['private_key_path']) 

    def build_request_param(self, **kwargs):
        paramters = self.para_filter(kwargs)
        sign = self.build_request_sign(paramters)
        paramters['sign'] = sign
        paramters['sign_type'] = 'RSA'
        print paramters
        return paramters

if __name__=='__main__':
    alipay_config = {
        'private_key_path': '/usr/local/paykey/alipay/rsa_private_key.pem'
    }
    paramters = {
        "partner" : '2088021002933404',
        "seller_id": 'tbkpay@7swim.com',
        'out_trade_no':'54ffsar23421',
        'subject': 'product_title',
        'body': 'product_body',
        'total_fee': 0.01,
        'notify_url': 'xxxxx.com',
        'service': 'mobile.securitypay.pay',
        'payment_type': '1',
        '_input_charset':'utf-8',
        'it_b_pay': "30m",
        'sign_type': "RSA"
    }
    api = AliApi(alipay_config)
    api.build_request_param(**paramters)

