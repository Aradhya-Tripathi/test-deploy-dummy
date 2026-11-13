from flask import Flask

from app import app, create_app


def test_homepage_returns_polished_content():
    client = create_app().test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Small app. Bright ideas." in response.data
    assert b"Built with Flask" in response.data
    assert b'href="/static/style.css"' in response.data


def test_module_exposes_wsgi_app():
    assert isinstance(app, Flask)
