#!/usr/bin/env python3
"""
Async routine that takes in 2 int arguments (n and max_delay) and spawns
wait_random n times with the specified max_delay.
"""

import asyncio
from typing import List


wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    Async routine that spawns wait_random n times with the specified
    max_delay and returns the list of all the delays.

    Parameters:
    - n (int): Number of times to spawn wait_random.
    - max_delay (int): Maximum delay for wait_random.

    Returns:
    - List[float]: List of delays (float values) in ascending order.
    """
    delays = [await wait_random(max_delay) for _ in range(n)]
    return sorted(delays)
