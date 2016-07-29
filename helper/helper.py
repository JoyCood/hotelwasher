#!/usr/bin/python 
# -*- coding: utf-8 -*-
from config import base

import httplib
import urllib
import json

def send_sms(text, mobile):
    params = {'apikey':base.YUNPIAN_API_KEY, 'text':text, 'mobile':mobile}
    params = urllib.urlencode(params)
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json", "charset":"utf-8"}
    conn = httplib.HTTPSConnection(base.YUNPIAN_HOST, base.YUNPIAN_PORT, timeout=base.YUNPIAN_TIMEOUT)
    conn.request("POST", '/v2/sms/single_send.json', params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str
