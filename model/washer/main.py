#!/usr/bin/python
# -*- coding: utf-8 -*-

from common import mongo

class Washer(object):
    
    @staticmethod
    def aggregate(pipline, **kwargs):
       return mongo.washer.aggregate(pipline, **args) 

    @staticmethod
    def insert_one(doc, bypass_document_validation=False):
        return mongo.washer.insert_one(doc, bypass_document_validation)

    @staticmethod
    def find_one(filter, *args, **kwargs):
        return mongo.washer.find_one(filter, *args, **kwargs)

    @staticmethod
    def update_one(filter, update, upsert=False, bypass_document_validation=False):
        return mongo.washer.update_one(filter, update, upsert, bypass_document_validation)
