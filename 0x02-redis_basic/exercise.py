#!/usr/bin/env python3
"""Writting strings to Redis"""
from typing import Union, Callable, Optional
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

    def get(self, key: str, fn: Optional[Callable] = None) -> str:
        """Convert data back to a desired format"""
        # if (!self._redis.exists(key))
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, data: str) -> str:
        """Parametrize Cache.get with conversion function"""
        return data.decode('utf-8', 'strict')

    def get_int(self, data: str) -> int:
        """Parametrize Cache.get with conversion function"""
        return int(data)
