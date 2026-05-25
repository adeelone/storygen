import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.errors import SafetyRefusal
from app.models import StreamEvent

router = APIRouter()


@router.websocket("/ws/{session_id}")
async def story_socket(websocket: WebSocket, session_id: str) -> None:
    await websocket.accept()
    repo = websocket.app.state.repo
    pipeline = websocket.app.state.pipeline
    sessions = websocket.app.state.sessions
    story = repo.get(session_id)
    if not story:
        await websocket.send_json({"type": "error", "data": {"message": "Story session not found."}})
        await websocket.close(code=1008)
        return

    for event in await sessions.replay(session_id):
        await websocket.send_json(event.model_dump(mode="json"))

    async def emit(event: StreamEvent) -> None:
        await sessions.append(event)
        await websocket.send_json(event.model_dump(mode="json"))

    async def listen() -> None:
        while True:
            payload = await websocket.receive_json()
            if payload.get("type") == "cancel":
                await sessions.cancel(session_id)
                return
            if payload.get("type") == "ping":
                await emit(StreamEvent(type="ping", session_id=session_id, data={"alive": True}))

    if story.status == "complete":
        await websocket.close()
        return
    listener = asyncio.create_task(listen())
    try:
        story = await pipeline.generate(story, emit, lambda: sessions.is_cancelled(session_id))
        repo.save(story)
    except SafetyRefusal as exc:
        await emit(
            StreamEvent(
                type="error",
                session_id=session_id,
                data={"message": exc.message, "suggested_rewrite": exc.rewrite, "friendly": True},
            )
        )
    except WebSocketDisconnect:
        pass
    except Exception as exc:
        await emit(
            StreamEvent(
                type="error",
                session_id=session_id,
                data={"message": "Story generation paused unexpectedly.", "detail": str(exc)},
            )
        )
    finally:
        listener.cancel()
        try:
            await websocket.close()
        except RuntimeError:
            pass
