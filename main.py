from functools import wraps
from inspect import iscoroutinefunction


class Cache:
    def __init__(self):
        self.data = {}

    def __call__(self, func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            if key in self.data:
                return self.data[key]
            result = await func(*args, **kwargs)
            self.data[key] = result
            return result

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            if key in self.data:
                return self.data[key]
            result = func(*args, **kwargs)
            self.data[key] = result
            return result

        return async_wrapper if iscoroutinefunction(func) else wrapper

    def invalidate(self, func):
        key_to_remove = [key for key in self.data if key[0] == func.__name__]
        for key in key_to_remove:
            del self.data[key]


cache = Cache()


@cache
def slow_function(arg):
    return arg


class MyClass:
    @cache
    def method(self, arg):
        return arg


@cache
async def async_func(arg):
    return arg
