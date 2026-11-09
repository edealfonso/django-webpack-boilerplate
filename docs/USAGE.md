# Usage

[Español](USAGE.es.md)

Reference for working with the boilerplate. Quick start: see the [README](../README.md).

## Project structure

- `myproject/`: the Django project
  - `config/`: settings (`base`, `local`, `prod`, `test`), urls, wsgi/asgi
  - `apps/`: example apps (`pages`, `content`) to start from. `models.py`/`admin.py` include a commented example using the editor and sortable admin
  - `static/`: Sass and JS sources (webpack builds them into `static/bundles/`)
  - `templates/`: Django templates (`templates/admin/base_site.html` adds `static/admin-custom/admin.css` to the admin)
  - `Dockerfile`, `compose.yml` (dev), `compose.prod.yml` (prod), `docker/`
- `manuals/ES/`: step-by-step guides in Spanish (all Docker-based)
  - `1_CREAR_NUEVO_PROYECTO.md`: new project, apps, migrations, dependencies
  - `2_DEPLOYMENT.md`: deploying to a VPS with HTTPS (host nginx + certbot)
  - `BASES_DE_DATOS_POSTGRES.md`: psql, dumps, restore, CSV import
  - `TRANSLATE.md`: i18n and django-modeltranslation

## Starting a new project

1. Copy this repo and rename `myproject` everywhere to your project's name (folder, `package.json`, `compose*.yml` defaults, `.env.example`, admin titles in `config/urls.py`).
2. Optionally copy `myproject/.env.example` to `myproject/.env`. In development every value has a default, so you can skip this step.

## Development

All commands are run from `myproject/`.

```bash
docker compose up --build             # start db + web + assets
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

- Site: http://localhost:8000. Admin: http://localhost:8000/admin/
- `web` runs `runserver` with the code bind-mounted, so Python and template changes reload automatically.
- `assets` runs webpack in watch mode: Sass/JS changes are rebuilt into `static/bundles/`. On the very first start, wait until webpack finishes, or the page will fail because `webpack-stats.json` does not exist yet (`docker compose logs -f assets`).
- The database lives in the `pgdata` volume. `docker compose down -v` wipes it.

Useful commands:

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py shell
docker compose run --rm assets npm install some-package   # add a JS dependency
docker compose build web                                   # after changing requirements.txt
docker compose logs -f web
```

Port conflicts: set `WEB_PORT=8001` (in `.env` or inline, e.g. `WEB_PORT=8001 docker compose up`). The database port is not published to the host. Uncomment `ports` under `db` in `compose.yml` if you need to reach it from a DB client.

## Frontend

- Entry point: `static/js/script.js`. It imports `static/scss/index.scss`. Templates load the result with `{% render_bundle 'main' 'css' %}` / `{% render_bundle 'main' 'js' %}`.
- One `webpack.config.js` for both modes: `npm run watch` (dev, run by the `assets` service) and `npm run build` (prod, run inside the Docker build).
- Sass uses the module system: `index.scss` loads the partials with `@use`, and each partial loads what it needs with `@use "variables" as *;` (or `"../variables"` from a subfolder).
- PostCSS (`postcss.config.js`) adds prefixes and modern CSS fallbacks. Babel (`babel.config.json`) transpiles JS. Both target the browsers in `browserslist` (`package.json`).
- Neutral starting point: system font stack and a small palette in `variables.scss`. Webfonts go in `static/fonts/` (`woff2` only) and are declared in `fonts.scss`. Fonts and images referenced from Sass are emitted to `static/bundles/assets/` with hashed names.
- Admin branding: uncomment the CSS variables in `static/admin-custom/admin.css`. Never copy Django's admin CSS files into `static/admin/`: they would override the admin's own CSS on every Django upgrade.
- No jQuery: plain JS. To add a library: `docker compose run --rm assets npm install <package>` and `import` it in `script.js`.

## Tests

```bash
docker compose exec web python manage.py test --settings=config.settings.test
```

`config.settings.test` uses in-memory SQLite and a fake webpack loader, so tests need neither Postgres nor a webpack build.

## Production

Run from `myproject/`:

```bash
cp .env.example .env    # then set SECRET_KEY, POSTGRES_*, ALLOWED_HOSTS (and CSRF_TRUSTED_ORIGINS)
docker compose -f compose.prod.yml up -d --build
docker compose -f compose.prod.yml exec web python manage.py createsuperuser
```

- `web`: multi-stage image (webpack production build + Python), gunicorn as a non-root user. `migrate` and `collectstatic` run on every start.
- `nginx`: listens on port 80 (`HTTP_PORT` to change it), serves `/static/` and `/media/` and proxies everything else to gunicorn.
- `db`: PostgreSQL with data in the `pgdata` volume. Uploaded files live in the `media` volume. Back both up.
- HTTPS is not included: terminate TLS in front of this stack (host nginx + certbot, Caddy, Traefik, or your provider's load balancer). Step-by-step guide with host nginx + certbot: `[manuals/ES/2_DEPLOYMENT.md](../manuals/ES/2_DEPLOYMENT.md)`. Set `HTTP_PORT=127.0.0.1:8080` so the stack is only reachable through that proxy.

To update: `git pull && docker compose -f compose.prod.yml up -d --build`.

## Configuration (`.env`)

| Variable | Dev | Prod | Notes |
|---|---|---|---|
| `SECRET_KEY` | optional | **required** | `docker compose run --rm web python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `POSTGRES_DB` / `POSTGRES_USER` / `POSTGRES_PASSWORD` | optional | **required** | Used by the `db` container and to build `DATABASE_URL`. Avoid `@ : / ? #` in the password. |
| `ALLOWED_HOSTS` | optional | **required** | Comma-separated |
| `CSRF_TRUSTED_ORIGINS` | – | recommended | e.g. `https://example.com,https://www.example.com` |
| `SECURE_HTTPS` | – | optional | Default `True`: HTTPS redirect + secure cookies. Set `False` only to try the prod stack over plain HTTP. |
| `SECURE_HSTS_SECONDS` | – | optional | Default `0`. Start with `3600`, raise to `31536000` once HTTPS is confirmed. |
| `WEB_PORT` / `HTTP_PORT` | optional | optional | Host ports (dev: 8000, prod: 80) |
| `DATABASE_URL` | – | – | Set by compose. Only needed when running Django outside Docker. |

Never commit `.env`.
