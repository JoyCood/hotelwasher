#!/usr/bin/python 
# -*- coding: utf-8 -*-

from common import mongo

class Order(object):

    @staticmethod
    def find(filter=None, projection=None, skip=0, sort=None, limit=0, no_cursor_timeout=False, cursor_type=CursorType.NON_TAILABLE, allow_partial_results=False, oplog_replay=False, modifiers=None, manipulate=True)
        return mongo.order.find(filter, projection, skip, limit, no_cursor_timeout, cursor_type=CursorType.NON_TAILABLE, sort, allow_partial_results, oplog_replay, modifiers, manipulate)
    
    @staticmethod
    def find_one(filter, *args, **kwargs)
        return mongo.order.find_one(filter, *args, **kwargs)

    @staticmethod
    def insert_one(doc, bypass_document_validation=False)
        return mongo.order.insert_one(doc, bypass_document_validation)

    @staticmethod
    def update_one(filter, update, upsert=False, bypass_document_validation=False):
        return mongo.order.update_one(filter, update, upsert, bypass_document_validation)
