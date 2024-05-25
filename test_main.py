import pytest
from main import cache, slow_function, MyClass, async_func
import asyncio


def test_cache():
    assert slow_function(1) == 1
    assert slow_function(1) == 1
    assert len(cache.data) == 1

    obj = MyClass()
    assert obj.method(1) == 1
    assert obj.method(1) == 1
    assert len(cache.data) == 2

    cache.invalidate(slow_function)
    assert len(cache.data) == 1


@pytest.mark.asyncio
async def test_cache_async():
    assert await async_func(1) == 1
    assert await async_func(1) == 1
    assert len(cache.data) == 1

    cache.invalidate(async_func)
    assert len(cache.data) == 0
