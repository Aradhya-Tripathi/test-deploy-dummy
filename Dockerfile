# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12
ARG NODE_VERSION=22

# 1. Bundle and minify frontend assets.
FROM docker.io/library/node:${NODE_VERSION}-alpine AS assets
WORKDIR /src
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --ignore-scripts --no-audit --no-fund
COPY frontend ./frontend
RUN npm run build

# 2. Resolve Python dependencies into a relocatable virtualenv.
FROM docker.io/library/python:${PYTHON_VERSION}-slim AS deps
COPY --from=ghcr.io/astral-sh/uv:0.9 /uv /usr/local/bin/uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    VIRTUAL_ENV=/opt/venv
RUN uv venv /opt/venv
COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --python /opt/venv/bin/python -r requirements.txt

# 3. Run the test suite; a failure here fails the build and blocks the release.
FROM deps AS test
WORKDIR /src
COPY requirements.txt requirements-dev.txt ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --python /opt/venv/bin/python -r requirements-dev.txt
COPY app.py gunicorn.conf.py ./
COPY templates ./templates
COPY tests ./tests
COPY --from=assets /src/static/dist ./static/dist
RUN /opt/venv/bin/python -m pytest -q -p no:cacheprovider \
    && touch /tests-passed

# 4. Stamp the commit and build time. Push-to-deploy checks out a detached HEAD, so .git/HEAD is the SHA.
FROM docker.io/library/busybox:1.37 AS meta
COPY .git/HEAD /git-head
RUN head="$(cat /git-head)"; \
    case "$head" in ref:*) commit=dev ;; *) commit="$head" ;; esac; \
    printf '{"commit": "%s", "built_at": "%s"}\n' "$commit" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > /build-info.json \
    && cat /build-info.json

# 5. Minimal runtime: no build tools, no tests, non-root.
FROM docker.io/library/python:${PYTHON_VERSION}-slim AS runtime
LABEL org.opencontainers.image.title="brightside" \
      org.opencontainers.image.description="Deploy inspector for push-to-deploy"
ENV PATH=/opt/venv/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    BUILD_INFO_PATH=/app/build-info.json
RUN groupadd --system --gid 10001 app \
    && useradd --system --uid 10001 --gid app --home-dir /app --shell /usr/sbin/nologin app
WORKDIR /app
COPY --from=deps /opt/venv /opt/venv
COPY --chown=app:app app.py gunicorn.conf.py ./
COPY --chown=app:app templates ./templates
COPY --from=assets --chown=app:app /src/static/dist ./static/dist
COPY --from=meta /build-info.json ./build-info.json
# Depending on the test stage forces it to run before the runtime image exists.
COPY --from=test /tests-passed /tmp/tests-passed
USER app
EXPOSE 8000
STOPSIGNAL SIGTERM
CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:app"]
