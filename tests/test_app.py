import json

from flask import Flask

from app import app, create_app


def make_client(tmp_path, monkeypatch, port="8002"):
    monkeypatch.setenv("PORT", port)
    build_info = tmp_path / "build-info.json"
    build_info.write_text(json.dumps({"commit": "abc123def4567890", "built_at": "2026-11-25T10:00:00Z"}))
    return create_app(build_info).test_client()


def test_homepage_shows_release(tmp_path, monkeypatch):
    response = make_client(tmp_path, monkeypatch).get("/")

    assert response.status_code == 200
    assert b"git push." in response.data
    assert b"Push to Deploy" in response.data
    assert b"abc123def456" in response.data
    assert b'data-slot="green"' in response.data
    assert b'href="/static/dist/app.css"' in response.data


def test_api_info_reports_slot_and_build(tmp_path, monkeypatch):
    info = make_client(tmp_path, monkeypatch, port="8001").get("/api/info").get_json()

    assert info["slot"] == "blue"
    assert info["port"] == "8001"
    assert info["build"]["commit"] == "abc123def4567890"
    assert info["uptime_seconds"] >= 0


def test_health_returns_commit(tmp_path, monkeypatch):
    response = make_client(tmp_path, monkeypatch).get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok", "commit": "abc123def4567890"}


def test_missing_build_info_falls_back_to_dev(tmp_path, monkeypatch):
    monkeypatch.setenv("PORT", "5000")
    info = create_app(tmp_path / "missing.json").test_client().get("/api/info").get_json()

    assert info["build"]["commit"] == "dev"
    assert info["slot"] == "local"


def test_module_exposes_wsgi_app():
    assert isinstance(app, Flask)
