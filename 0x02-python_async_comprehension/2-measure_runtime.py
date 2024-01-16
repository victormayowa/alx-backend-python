#!/usr/bin/env python3
"""
Module with measure_runtime coroutine.
"""

from time import time
from asyncio import gather
from typing import List


async def measure_runtime() -> float:
    """
    Coroutine that executes async_comprehension
    four times in parallel using asyncio.gather
    and measures the total runtime.
    """
    start_time = time()
    await gather(*(async_comprehension() for _ in range(4)))
    end_time = time()
    return end_time - start_time
