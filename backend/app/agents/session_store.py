from collections import defaultdict
from datetime import UTC, datetime, timedelta

from app.models import StreamEvent


class SessionEventStore:
    def __init__(self) -> None:
        self.events: dict[str, list[StreamEvent]] = defaultdict(list)
        self.cancelled: set[str] = set()

    async def append(self, event: StreamEvent) -> None:
        cutoff = datetime.now(UTC) - timedelta(minutes=5)
        self.events[event.session_id] = [
            existing for existing in self.events[event.session_id] if existing.emitted_at > cutoff
        ] + [event]

    async def replay(self, session_id: str) -> list[StreamEvent]:
        cutoff = datetime.now(UTC) - timedelta(minutes=5)
        return [event for event in self.events.get(session_id, []) if event.emitted_at > cutoff]

    async def cancel(self, session_id: str) -> None:
        self.cancelled.add(session_id)

    def is_cancelled(self, session_id: str) -> bool:
        return session_id in self.cancelled
