# Dummy Flask App Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a tested, database-free Flask landing page that is ready for local use and simple deployment.

**Architecture:** A Flask app factory owns the single route and renders a Jinja template. Static CSS owns presentation; the Python layer remains intentionally small.

**Tech Stack:** Python 3, Flask 3, Jinja, CSS, pytest

**Spec:** `docs/superpowers/specs/2026-11-13-dummy-flask-design.md`

## Global Constraints

- No database or persistence.
- No external frontend dependencies.
- Serve the home page at `/`.

## Review Focus

- The root route must return HTTP 200 and meaningful page copy.
- The generated HTML must reference the local stylesheet.
- The package must expose a WSGI-compatible `app` object.

---

### Task 1: Homepage application

**Files:**
- Create: `app.py`
- Create: `templates/index.html`
- Create: `static/style.css`
- Create: `requirements.txt`
- Create: `README.md`
- Create: `.gitignore`
- Test: `tests/test_app.py`

**Interfaces:**
- Consumes: HTTP GET `/`
- Produces: `create_app()` and module-level Flask `app`

- [ ] Write tests asserting HTTP 200, key page copy, stylesheet reference, and the module-level app.
- [ ] Run `.venv/bin/pytest -q` and confirm failure because `app.py` does not exist.
- [ ] Implement the app, template, stylesheet, dependencies, documentation, and ignore rules.
- [ ] Run `.venv/bin/pytest -q` and confirm all tests pass.
- [ ] Commit the verified implementation.

