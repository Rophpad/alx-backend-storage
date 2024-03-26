#!/usr/bin/env python3
"""Insert a document in Python"""
import pymongo


def insert_school(mongo_collection, **kwargs):
    """Insert a new document in mongo_collection"""
    return mongo_collection.insert_one(kwargs).inserted_id
