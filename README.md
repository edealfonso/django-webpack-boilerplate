# Django Webpack Boilerplate

[English](README.md) · [Español](README.es.md)

![Django admin with rich text editor and sortable list, and docker compose up starting the stack](docs/screenshot.png)

A starter template for Django projects with a modern frontend build. Instead of setting up Django, Webpack, Sass, PostgreSQL, nginx and HTTPS from scratch on every project, you copy this repo, rename it and run `docker compose up`: the database, the Django dev server and webpack in watch mode start together, with nothing installed on your machine except Docker. The same repo deploys to production with one command.

## Features

- **One-command dev environment**: PostgreSQL, Django `runserver` with auto-reload, and webpack rebuilding Sass/JS on every change.
- **Production stack**: multi-stage Docker image, gunicorn as a non-root user, nginx serving static and media files, automatic migrations and `collectstatic`.
- **Secure by default**: configuration and secrets in `.env`, HTTPS redirect, secure cookies and opt-in HSTS in production.
- **Admin ready for content**: rich text editor with server-side HTML sanitization, and drag & drop ordering of lists. Includes a commented example model.
- **Tested**: test settings that need neither Postgres nor a webpack build.
- **Documented**: step-by-step guides (in Spanish) for new projects, VPS deployment with HTTPS, Postgres dumps and translations.

## Tech stack

| Area | Technologies |
|---|---|
| Backend | Python 3.13, Django 5.2 LTS, PostgreSQL 17 (psycopg 3), django-environ, django-webpack-loader, [django-prose-editor](https://github.com/matthiask/django-prose-editor), [django-admin-sortable2](https://github.com/jrief/django-admin-sortable2) |
| Frontend | Webpack 5, Sass (`@use` modules), PostCSS (postcss-preset-env), Babel, Node 24 |
| Infrastructure | Docker, Docker Compose, gunicorn, nginx |

## Quick start

Requires only [Docker](https://docs.docker.com/get-docker/) (with Compose v2).

```bash
git clone https://github.com/edealfonso/django-webpack-boilerplate.git
cd django-webpack-boilerplate/myproject
docker compose up --build
# in another terminal, once webpack has finished:
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

Open http://localhost:8000 (admin at `/admin/`). To start your own project, rename `myproject` everywhere ([details](docs/USAGE.md#starting-a-new-project)).

## Documentation

- [Usage reference](docs/USAGE.md): project structure, development, frontend, tests, production and `.env` settings.
- Step-by-step guides (in Spanish): [new project](manuals/ES/1_CREAR_NUEVO_PROYECTO.md), [VPS deployment with HTTPS](manuals/ES/2_DEPLOYMENT.md), [Postgres](manuals/ES/BASES_DE_DATOS_POSTGRES.md), [translations](manuals/ES/TRANSLATE.md).

## Demo

No online demo: this is a template, not an app. The screenshot above shows what you get after `docker compose up` (Django admin with the example model enabled).

## My contribution

- Started from the boilerplate we used at my studio, and cleaned it up, removing everything that wasn't needed.
- Wrote the step-by-step manuals (`manuals/ES/`).
- In 2026 I updated and improved it with the help of [Claude Code](https://claude.com/claude-code): Docker for development and production, Django 5.2 LTS, security (secrets out of the repo, HTTPS settings), a modernized frontend build and documentation rewritten for Docker.

## Roadmap

- [ ] CI with GitHub Actions: run the tests and build the Docker images on every push
- [ ] [Ruff](https://docs.astral.sh/ruff/) as Python linter and formatter
- [ ] Dependabot: automatic update PRs for pip, npm and Docker images
