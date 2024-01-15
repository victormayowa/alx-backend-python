#!/usr/bin/env python3
"""
Module with task_wait_n function.
"""

import asyncio
from typing import List
from random import uniform


async def wait_random(max_delay: int = 10) -> float:
    """
    Asynchronous coroutine that takes in an integer argument max_delay
    (with a default value of 10) named wait_random that waits for a random
    delay between 0 and max_delay (included and float value) seconds and
    eventually returns it.
    """
    delay = uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay


async def task_wait_random(max_delay: int) -> float:
    """
    Asynchronous coroutine that calls wait_random.
    """
    return await wait_random(max_delay)


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
    Asynchronous coroutine that spawns task_wait_random n times
    with the specified
    max_delay.
    """
    tasks = [task_wait_random(max_delay) for _ in range(n)]
    return await asyncio.gather(*tasks)
