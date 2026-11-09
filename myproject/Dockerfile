# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.13
ARG NODE_VERSION=24


# ---------------------------------------------------------------------------
# assets: build the frontend bundles with webpack (used by the prod image)
# ---------------------------------------------------------------------------
FROM node:${NODE_VERSION}-slim AS assets

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY webpack.config.js postcss.config.js babel.config.json ./
COPY static ./static
RUN npm run build


# ---------------------------------------------------------------------------
# base: Python + dependencies
# ---------------------------------------------------------------------------
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt


# ---------------------------------------------------------------------------
# dev: source code is bind-mounted by compose.yml
# ---------------------------------------------------------------------------
FROM base AS dev

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# ---------------------------------------------------------------------------
# prod: code + built assets, gunicorn, non-root user
# ---------------------------------------------------------------------------
FROM base AS prod

ENV DJANGO_SETTINGS_MODULE=config.settings.prod

RUN useradd --create-home --uid 1000 app \
    && mkdir -p /app/staticfiles /app/media \
    && chown app:app /app/staticfiles /app/media

COPY --chown=app:app . .
COPY --from=assets --chown=app:app /app/static/bundles ./static/bundles
COPY --from=assets --chown=app:app /app/webpack-stats.json ./webpack-stats.json
RUN chmod +x docker/entrypoint.prod.sh

USER app
EXPOSE 8000
ENTRYPOINT ["docker/entrypoint.prod.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--access-logfile", "-"]
