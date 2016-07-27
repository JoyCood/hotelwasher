#!/usr/bin/python
# -*- coding: utf-8 -*-

from common import mongo

class Member_Mix(object):
    def find_one(filter, *args, **kwargs):
        return mongo.member_mix.find_one(filter, *args, **kwargs)
