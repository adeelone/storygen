from fastapi.testclient import TestClient

from app.main import create_app
from tests.helpers import workspace_tmp


def test_prompt_streams_complete_story() -> None:
    client = TestClient(create_app(workspace_tmp("websocket-complete")))
    story = client.post("/api/v1/stories", json={"prompt": "a squirrel and a robot save lantern light"}).json()
    events: list[str] = []
    with client.websocket_connect(f"/ws/{story['id']}") as socket:
        while "story_complete" not in events:
            events.append(socket.receive_json()["type"])
    assert events.count("scene_complete") == 4
    assert "plan_ready" in events
    assert "character_sheet" in events
    saved = client.get(f"/api/v1/stories/{story['id']}").json()
    assert saved["status"] == "complete"
