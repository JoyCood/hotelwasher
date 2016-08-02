#!/usr/bin/python
# -*- coding: utf-8 -*-

from common import mongo

class Washer_Mix(object):
    @staticmethod
    def find_one(filter, *args, **kwargs):
        return mongo.washer_mix.find_one(filter, *args, **kwargs)

    @staticmethod
    def insert_one(doc, bypass_document_validation=False):
        return mongo.washer_mix.insert_one(doc, bypass_document_validation)

    @staticmethod
    def update_one(filter, update, upsert=False, bypass_document_validation=False):
        return mongo.washer_mix.update(filter, update, upsert, bypass_document_validation)
