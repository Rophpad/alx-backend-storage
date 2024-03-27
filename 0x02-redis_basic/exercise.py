#!/usr/bin/env python3
"""Writting strings to Redis"""
from typing import Union
import redis
import uuid

class Cache():
    """Cache class"""
    def __init__(self):
        """Store an instance of the Redis client"""
        self._redis = redis.Redis()
        self._redis.flushdb()


    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Generate random key"""
        key = str(uuid.uuid4())
        self._redis.mset({key: data})
        return key
