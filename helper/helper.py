#!/usr/bin/python 
# -*- coding: utf-8 -*-
from config import base

import httplib
import urllib
import string
import random
import logging

import phonenumbers

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-9s) %(message)s')

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

def verify_phone(phone, country='CN'):
    try:
        phone_number = phonenumbers.parse(phone, country)
    except phonenumbers.NumberParseException:
        return False
    return phonenumbers.is_valid_number(phone_number)
        

def get_random(size):
    chars = string.ascii_letters + string.digits
    return ''.join((random.choice(chars) for _ in range(size)))

def log(message):
    logging.debug(message)
