#!/usr/bin/env python3
"""
Module with async_generator coroutine.
"""

import asyncio
from typing import Generator
from random import uniform


async def async_generator() -> Generator[float, None, None]:
    """
    Coroutine that loops 10 times, each time asynchronously waiting 1 second,
    then yielding a random number between 0 and 10.
    """
    for _ in range(10):
        await asyncio.sleep(1)
        yield uniform(0, 10)
