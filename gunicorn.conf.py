import os

bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"
workers = int(os.environ.get("WEB_CONCURRENCY", "2"))
threads = int(os.environ.get("GUNICORN_THREADS", "4"))
worker_class = "gthread"
graceful_timeout = 20
accesslog = "-"
errorlog = "-"
forwarded_allow_ips = "127.0.0.1"
