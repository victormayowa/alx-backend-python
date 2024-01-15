#!/usr/bin/env python3
"""
Module with task_wait_random function that returns an asyncio.Task.
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


def task_wait_random(max_delay: int) -> asyncio.Task:
    """
    Regular function syntax that takes an integer max_delay and returns
    an asyncio.Task.
    """
    return asyncio.create_task(wait_random(max_delay))
