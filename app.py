import json
import os
import platform
import socket
import time
from pathlib import Path

from flask import Flask, jsonify, render_template

STARTED_AT = time.time()
SLOTS = {"8001": "blue", "8002": "green"}
DEFAULT_BUILD_INFO_PATH = Path(__file__).with_name("build-info.json")


def load_build_info(path: Path) -> dict:
    """Build metadata baked in by the Dockerfile; `dev` when run from a checkout."""
    if not path.exists():
        return {"commit": "dev", "built_at": None}
    return json.loads(path.read_text())


def get_runtime_info(build: dict) -> dict:
    port = os.environ.get("PORT", "5000")
    return {
        "build": build,
        "slot": SLOTS.get(port, "local"),
        "port": port,
        "hostname": socket.gethostname(),
        "python": platform.python_version(),
        "pid": os.getpid(),
        "uptime_seconds": int(time.time() - STARTED_AT),
    }


def create_app(build_info_path: Path | None = None) -> Flask:
    app = Flask(__name__)
    build = load_build_info(build_info_path or Path(os.environ.get("BUILD_INFO_PATH", DEFAULT_BUILD_INFO_PATH)))

    @app.get("/")
    def home() -> str:
        return render_template("index.html", info=get_runtime_info(build))

    @app.get("/api/info")
    def info():
        return jsonify(get_runtime_info(build))

    @app.get("/health")
    def health():
        return jsonify(status="ok", commit=build["commit"])

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
