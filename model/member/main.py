#!/usr/bin/python 
# -*- coding: utf-8 -*-

from common import mongo
from pymongo.errors import (
         DuplicateKeyError
        ,DocumentTooLarge
        ,ExecutionTimeout
        ,ConnectionFailure)

class Member(object):
    @staticmethod
    def find_one(filter, *args, **kwargs):
        return mongo.member.find_one(filter,*args, **kwargs)
    
    @staticmethod
    def insert_one(doc, bypass_document_validation=False):
        return mongo.member.insert_one(doc, bypass_document_validation)
        
    @staticmethod
    def update_one(filter, update, upsert=False, bypass_document_validation=False):
        return mongo.member.update_one(filter, update, upsert, bypass_document_validation)
