#!/usr/bin/python
# -*- coding: utf-8 -*-

from base import Base
import xmltodict
import json

class Result(Base):

    def parse_xml(self):
        self.values = json.dumps(xmltodict.parse(self.values))
        self.values = json.loads(self.values)
        self.values = self.values['xml']
        if self.values['result_code'] != 'SUCCESS':
            return self.values
        self.check_sign()
        return self.get_values()
    
    def check_sign(self):
        if not self.is_sign_set():
            print 'sig not set'
            raise
        sign = self.make_sign()
        if self.get_sign() == sign:
            return True
        raise
