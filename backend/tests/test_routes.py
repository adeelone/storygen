from pathlib import Path

from fastapi.testclient import TestClient

from app.main import create_app


def complete_story(client: TestClient) -> dict[str, object]:
    story = client.post("/api/v1/stories", json={"prompt": "a star lantern"}).json()
    with client.websocket_connect(f"/ws/{story['id']}") as socket:
        while socket.receive_json()["type"] != "story_complete":
            pass
    return client.get(f"/api/v1/stories/{story['id']}").json()


def test_library_share_exports_rerolls_and_admin(tmp_path: Path) -> None:
    app = create_app(tmp_path)
    app.state.settings.admin_key = "test-admin"
    client = TestClient(app)
    story = complete_story(client)
    story_id = story["id"]

    assert client.get("/api/v1/stories", params={"q": "star"}).json()[0]["id"] == story_id
    shared = client.post(f"/api/v1/stories/{story_id}/share", json={"expires_days": 2}).json()
    assert client.get(f"/api/v1/shares/{shared['slug']}").status_code == 200
    assert client.delete(f"/api/v1/stories/{story_id}/share").json()["public"] is False
    assert client.get(f"/api/v1/shares/{shared['slug']}").status_code == 404

    assert client.post(f"/api/v1/stories/{story_id}/scenes/1/image", json={"tweak": "more stars"}).status_code == 200
    assert client.post(f"/api/v1/stories/{story_id}/scenes/1/regenerate").status_code == 200
    assert client.get(f"/api/v1/stories/{story_id}/export.pdf").content.startswith(b"%PDF")
    assert client.get(f"/api/v1/stories/{story_id}/export.epub").content.startswith(b"PK")
    assert client.post(f"/api/v1/stories/{story_id}/narration").status_code == 200

    assert client.get("/api/v1/admin/usage").status_code == 403
    assert client.get("/api/v1/admin/usage", headers={"x-admin-key": "test-admin"}).json()["stories_today"] == 1
    assert client.get("/api/v1/admin/eval", headers={"x-admin-key": "test-admin"}).json()["passed"] is True


def test_missing_records_and_friendly_safety_refusal(tmp_path: Path) -> None:
    client = TestClient(create_app(tmp_path))
    assert client.get("/api/v1/stories/missing").status_code == 404
    assert client.get("/api/v1/stories/missing/export.pdf").status_code == 404
    assert client.post("/api/v1/stories/missing/narration").status_code == 404

    story = client.post("/api/v1/stories", json={"prompt": "a weapon in the garden", "age_band": "3-5"}).json()
    with client.websocket_connect(f"/ws/{story['id']}") as socket:
        event = socket.receive_json()
    assert event["type"] == "error"
    assert event["data"]["friendly"] is True


def test_unknown_websocket_session_is_rejected(tmp_path: Path) -> None:
    client = TestClient(create_app(tmp_path))
    with client.websocket_connect("/ws/missing") as socket:
        assert socket.receive_json()["type"] == "error"


def test_anonymous_quota_is_enforced(tmp_path: Path) -> None:
    app = create_app(tmp_path)
    app.state.settings.anonymous_daily_quota = 1
    client = TestClient(app)
    assert client.post("/api/v1/stories", json={"prompt": "first"}).status_code == 200
    assert client.post("/api/v1/stories", json={"prompt": "second"}).status_code == 429
