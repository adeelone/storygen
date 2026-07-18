from fastapi.testclient import TestClient

from app.main import create_app
from tests.helpers import workspace_tmp


def complete_story(client: TestClient) -> dict[str, object]:
    story = client.post("/api/v1/stories", json={"prompt": "a star lantern"}).json()
    with client.websocket_connect(f"/ws/{story['id']}") as socket:
        while socket.receive_json()["type"] != "story_complete":
            pass
    return client.get(f"/api/v1/stories/{story['id']}").json()


def test_library_share_exports_rerolls_and_admin() -> None:
    app = create_app(workspace_tmp("routes-main"))
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


def test_missing_records_and_friendly_safety_refusal() -> None:
    client = TestClient(create_app(workspace_tmp("routes-missing")))
    assert client.get("/api/v1/stories/missing").status_code == 404
    assert client.get("/api/v1/stories/missing/export.pdf").status_code == 404
    assert client.post("/api/v1/stories/missing/narration").status_code == 404

    story = client.post("/api/v1/stories", json={"prompt": "a weapon in the garden", "age_band": "3-5"}).json()
    with client.websocket_connect(f"/ws/{story['id']}") as socket:
        event = socket.receive_json()
    assert event["type"] == "error"
    assert event["data"]["friendly"] is True


def test_unknown_websocket_session_is_rejected() -> None:
    client = TestClient(create_app(workspace_tmp("routes-websocket-missing")))
    with client.websocket_connect("/ws/missing") as socket:
        assert socket.receive_json()["type"] == "error"


def test_anonymous_quota_is_enforced() -> None:
    app = create_app(workspace_tmp("routes-quota"))
    app.state.settings.anonymous_daily_quota = 1
    client = TestClient(app)
    assert client.post("/api/v1/stories", json={"prompt": "first"}).status_code == 200
    assert client.post("/api/v1/stories", json={"prompt": "second"}).status_code == 429


def test_feature_flags_disable_optional_routes() -> None:
    app = create_app(workspace_tmp("routes-flags"))
    app.state.settings.enable_public_sharing = False
    app.state.settings.enable_pdf_export = False
    app.state.settings.enable_tts = False
    app.state.settings.enable_eval_dashboard = False
    app.state.settings.admin_key = "admin"
    client = TestClient(app)
    story = complete_story(client)
    story_id = story["id"]

    assert client.post(f"/api/v1/stories/{story_id}/share", json={}).status_code == 404
    assert client.get(f"/api/v1/stories/{story_id}/export.pdf").status_code == 404
    assert client.post(f"/api/v1/stories/{story_id}/narration").status_code == 404
    assert client.get("/api/v1/admin/eval", headers={"x-admin-key": "admin"}).status_code == 404


def test_admin_key_is_required_in_production() -> None:
    app = create_app(workspace_tmp("routes-admin-production"))
    app.state.settings.app_env = "production"
    app.state.settings.admin_key = None
    client = TestClient(app)
    assert client.get("/api/v1/admin/usage").status_code == 503
