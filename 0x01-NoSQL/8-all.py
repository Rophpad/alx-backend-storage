#!/usr/bin/env python3
"""Python function using pymongo"""
import pymongo


def list_all(mongo_collection):
    """List all dics in a collection"""
    return [] if (mongo_collection == None) else list(mongo_collection.find())
