# Push to Deploy demo

A small Flask app for showcasing Frappe Cloud Push to Deploy. The page shows the commit, build time, and blue/green slot answering the request, and pops a banner when a new release goes live.

## Endpoints

- `/`: the demo page.
- `/api/info`: commit, build time, slot, uptime, container hostname.
- `/health`: health check for the release step.

## Image

The `Dockerfile` has five stages: `assets` (esbuild), `deps` (uv virtualenv), `test` (pytest gate; a failing test fails the build), `meta` (stamps the commit from the detached `.git/HEAD`), and `runtime` (slim, non-root gunicorn on `$PORT`). It builds with `buildah build --layers` or Docker with BuildKit.

## Run locally

```bash
npm ci && npm run build
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
PORT=8001 .venv/bin/gunicorn -c gunicorn.conf.py app:app
```

`PORT=8001` shows the blue slot and `PORT=8002` the green one.

## Test

```bash
.venv/bin/python -m pytest
```
