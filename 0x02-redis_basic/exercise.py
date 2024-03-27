#!/usr/bin/env python3
"""Redis basics"""
from typing import Union, Callable, Optional
import redis
import uuid
from functools import wraps


def call_history(method: Callable) -> Callable:
    """Stores the history of inputs and outputs for a particular function"""
    method_key = method.__qualname__
    inputs = method_key + ':inputs'
    outputs = method_key + ':outputs'

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(inputs, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(result))
        return result
    return wrapper


def count_calls(method: Callable) -> Callable:
    """Counts number of times methods of Cache class are called"""
    method_key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(method_key)
        return method(self, *args, **kwargs)
    return wrapper


def replay(method: Callable) -> None:
    """Displays the history of calls of a particular function"""
    method_key = method.__qualname__
    inputs = method_key + 'inputs'
    outputs = method_key + 'outputs'
    redis = method.__self__._redis
    method_count = redis.get(method_key).decode('utf-8')
    print(f'{method_key} was called {method_count} times:')
    IOTuple = zip(redis.lrange(inputs, 0, -1), redis.lrange(outputs, 0, -1))
    for inp, outp in list(IOTuple):
        attr, data = inp.decode("utf-8"), outp.decode("utf-8")
        print(f'{method_key}(*{attr}) -> {data}')


class Cache():
    """Cache class"""
    def __init__(self):
        """Store an instance of the Redis client"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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
