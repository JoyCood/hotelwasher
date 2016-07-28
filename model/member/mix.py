#!/usr/bin/python
# -*- coding: utf-8 -*-

from common import mongo

class Member_Mix(object):
    @staticmethod
    def find_one(filter, *args, **kwargs):
        return mongo.member_mix.find_one(filter, *args, **kwargs)

    @staticmethod
    def insert_one(doc, bypass_document_validation=False):
        return mongo.member_mix.insert_one(doc, bypass_document_validation)

    @staticmethod
    def update_one(filter, update, upsert=False, bypass_document_validation=False):
        return mongo.member_mix.update_one(filter, update, upsert, bypass_document_validation)

