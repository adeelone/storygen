from pathlib import Path

from app.core.rate_limit import CircuitBreaker, TokenBucket, with_backoff
from app.exports import render_epub, render_pdf
from app.models import PromptInput, StoryRecord
from app.providers.safety.rules import RulesSafetyProvider
from app.storage.local import LocalStorage


def test_rate_limiter_and_circuit_breaker() -> None:
    bucket = TokenBucket(capacity=1, refill_rate=0)
    assert bucket.consume()
    assert not bucket.consume()
    circuit = CircuitBreaker(failure_threshold=1)
    circuit.failure()
    assert not circuit.available
    circuit.success()
    assert circuit.available


async def test_backoff_returns_after_retry() -> None:
    attempts = 0

    async def operation() -> str:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise RuntimeError("retry")
        return "done"

    assert await with_backoff(operation) == "done"


async def test_safety_age_rule() -> None:
    provider = RulesSafetyProvider()
    assert (await provider.screen("a bright picnic", "3-5"))[0]
    assert not (await provider.screen("a weapon in the garden", "3-5"))[0]


def test_signed_url_is_stable(tmp_path: Path) -> None:
    storage = LocalStorage(tmp_path)
    assert storage.signed_url("a.svg", 60) == storage.signed_url("a.svg", 60)


def test_export_formats() -> None:
    story = StoryRecord(slug="sample", request=PromptInput(prompt="stars"))
    assert render_pdf(story).startswith(b"%PDF")
    assert render_epub(story).startswith(b"PK")
