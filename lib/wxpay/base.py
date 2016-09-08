#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import string
import random
import hashlib
import httplib
import xmltodict


class Base(object):
    def __init__(self, appkey, values):
        self.appkey = appkey
        self.values = values

    def set_sign(self):
        self.values['sign'] = self.make_sign()

    def get_sign(self):
        return self.values['sign']

    def is_sign_set(self):
        return "sign" in self.values

    def get_values(self):
        return self.values

    def make_sign(self):
        paramters = self.to_url_params() + "&key=" + self.appkey
        md5 = hashlib.md5()
        md5.update(paramters)
        sign = md5.hexdigest()
        return sign.upper()

    def to_url_params(self):
        paramters = sorted(self.values.items())
        buf = list()
        for paramter, value in paramters:
            if paramter != 'sign' and value != '' and not isinstance(value, (list, dict)):
                buf.append(paramter)
                buf.append('=')
                buf.append(str(value))
                buf.append('&')

        url =  ''.join(buf).strip('&')
        return url

    def get_nonce_str(self, size=6):
        chars = string.ascii_letters + string.digits
        signature =  ''.join((random.choice(chars) for _ in range(size)))
        md5 = hashlib.md5()
        md5.update(signature)
        return md5.hexdigest()

    def to_xml(self):
        if not isinstance(self.values, (list, dict)) or len(self.values)<=0:
            raise
        values = sorted(self.values.items())
        xml = ["<xml>"]
        for paramter, value in values:
            if self.isnumeric(value):
                xml.append("<"+paramter+">")
                xml.append(str(value))
                xml.append("</"+paramter+">")
            else:
                xml.append("<"+paramter+">")
                xml.append("<![CDATA[" + value + "]]></"+paramter+">")
        xml.append("</xml>")
        return ''.join(xml)
    
    def isnumeric(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def post_xml(self, xml, url):
        conn = httplib.HTTPSConnection(url)
        conn.request("POST", '/pay/unifiedorder', xml)
        response = conn.getresponse()
        response_str = response.read()
        conn.close()
        return response_str
