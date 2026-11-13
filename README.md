# Dummy Flask App

A polished, database-free Flask landing page.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

Open <http://127.0.0.1:5000>.

## Test

```bash
pip install pytest
python -m pytest
```

## Deploy

Use `gunicorn app:app` as the start command on any Python-compatible hosting provider.
