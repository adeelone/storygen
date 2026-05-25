import asyncio
import random
import time
from dataclasses import dataclass
from typing import Awaitable, Callable, TypeVar

T = TypeVar("T")


@dataclass
class TokenBucket:
    capacity: int
    refill_rate: float
    tokens: float | None = None
    updated_at: float | None = None

    def __post_init__(self) -> None:
        self.tokens = float(self.capacity) if self.tokens is None else self.tokens
        self.updated_at = time.monotonic() if self.updated_at is None else self.updated_at

    def consume(self, amount: float = 1) -> bool:
        now = time.monotonic()
        assert self.updated_at is not None and self.tokens is not None
        self.tokens = min(self.capacity, self.tokens + (now - self.updated_at) * self.refill_rate)
        self.updated_at = now
        if self.tokens < amount:
            return False
        self.tokens -= amount
        return True


@dataclass
class CircuitBreaker:
    failure_threshold: int = 3
    recovery_seconds: int = 30
    failures: int = 0
    opened_at: float | None = None

    @property
    def available(self) -> bool:
        if self.opened_at is None:
            return True
        if time.monotonic() - self.opened_at > self.recovery_seconds:
            self.failures = 0
            self.opened_at = None
            return True
        return False

    def success(self) -> None:
        self.failures = 0
        self.opened_at = None

    def failure(self) -> None:
        self.failures += 1
        if self.failures >= self.failure_threshold:
            self.opened_at = time.monotonic()


async def with_backoff(operation: Callable[[], Awaitable[T]], attempts: int = 3) -> T:
    for attempt in range(attempts):
        try:
            return await operation()
        except Exception:
            if attempt == attempts - 1:
                raise
            await asyncio.sleep((2**attempt) * 0.15 + random.random() * 0.1)
    raise RuntimeError("unreachable")
