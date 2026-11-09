# Uso

[English](USAGE.md)

Referencia para trabajar con el boilerplate. Para arrancar rápido, mira el [README](../README.es.md).

## Estructura del proyecto

- `myproject/`: el proyecto de Django
  - `config/`: settings (`base`, `local`, `prod`, `test`), urls, wsgi/asgi
  - `apps/`: apps de ejemplo (`pages`, `content`) como punto de partida. `models.py`/`admin.py` incluyen un ejemplo comentado con el editor y el admin ordenable
  - `static/`: fuentes de Sass y JS (webpack las compila en `static/bundles/`)
  - `templates/`: plantillas de Django (`templates/admin/base_site.html` añade `static/admin-custom/admin.css` al admin)
  - `Dockerfile`, `compose.yml` (desarrollo), `compose.prod.yml` (producción), `docker/`
- `docs/manuals/ES/`: guías paso a paso (todas con Docker)
  - `1_CREAR_NUEVO_PROYECTO.md`: proyecto nuevo, apps, migraciones, dependencias
  - `2_DEPLOYMENT.md`: deployment en un VPS con HTTPS (nginx del host + certbot)
  - `BASES_DE_DATOS_POSTGRES.md`: psql, dumps, restaurar, importar CSV
  - `TRANSLATE.md`: traducciones e i18n con django-modeltranslation

## Empezar un proyecto nuevo

1. Copiar este repo y cambiar `myproject` por el nombre de tu proyecto en todas partes (carpeta, `package.json`, valores por defecto de `compose*.yml`, `.env.example`, títulos del admin en `config/urls.py`).
2. Opcionalmente, copiar `myproject/.env.example` a `myproject/.env`. En desarrollo todo tiene valor por defecto, así que este paso se puede saltar.

## Desarrollo

Todos los comandos se ejecutan desde `myproject/`.

```bash
docker compose up --build             # arranca db + web + assets
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

- Web: http://localhost:8000. Admin: http://localhost:8000/admin/
- `web` ejecuta `runserver` con el código montado como volumen: los cambios en Python y en las plantillas se recargan solos.
- `assets` ejecuta webpack en modo watch: los cambios en Sass/JS se recompilan en `static/bundles/`. La primera vez hay que esperar a que webpack termine; si no, la página da error porque todavía no existe `webpack-stats.json` (`docker compose logs -f assets`).
- La base de datos vive en el volumen `pgdata`. `docker compose down -v` la borra.

Comandos útiles:

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py shell
docker compose run --rm assets npm install some-package   # añadir una dependencia JS
docker compose build web                                   # después de cambiar requirements.txt
docker compose logs -f web
```

Si el puerto está ocupado, usa `WEB_PORT=8001` (en `.env` o en la propia línea, por ejemplo `WEB_PORT=8001 docker compose up`). El puerto de la base de datos no se publica en el host. Si necesitas conectarte con un cliente de BD, descomenta `ports` en el servicio `db` de `compose.yml`.

## Frontend

- Punto de entrada: `static/js/script.js`, que importa `static/scss/index.scss`. Las plantillas cargan el resultado con `{% render_bundle 'main' 'css' %}` / `{% render_bundle 'main' 'js' %}`.
- Un solo `webpack.config.js` para los dos modos: `npm run watch` (desarrollo, lo ejecuta el servicio `assets`) y `npm run build` (producción, se ejecuta dentro del build de Docker).
- Sass usa el sistema de módulos: `index.scss` carga los parciales con `@use`, y cada parcial carga lo que necesita con `@use "variables" as *;` (o `"../variables"` desde una subcarpeta).
- PostCSS (`postcss.config.js`) añade prefijos y alternativas para CSS moderno. Babel (`babel.config.json`) transpila el JS. Los dos apuntan a los navegadores de `browserslist` (`package.json`).
- Punto de partida neutro: fuentes del sistema y una paleta mínima en `variables.scss`. Las webfonts van en `static/fonts/` (solo `woff2`) y se declaran en `fonts.scss`. Las fuentes e imágenes que se referencian desde Sass se generan en `static/bundles/assets/` con hash en el nombre.
- Colores del admin: descomentar las variables CSS de `static/admin-custom/admin.css`. No copies nunca los CSS del admin de Django a `static/admin/`: sobrescribirían los del propio admin en cada actualización de Django.
- Sin jQuery: JS normal. Para añadir una librería: `docker compose run --rm assets npm install <paquete>` e importarla en `script.js`.

## Tests

```bash
docker compose exec web python manage.py test --settings=config.settings.test
```

`config.settings.test` usa SQLite en memoria y un loader falso de webpack, así que los tests no necesitan ni Postgres ni el build de webpack.

## Producción

Desde `myproject/`:

```bash
cp .env.example .env    # y rellenar SECRET_KEY, POSTGRES_*, ALLOWED_HOSTS (y CSRF_TRUSTED_ORIGINS)
docker compose -f compose.prod.yml up -d --build
docker compose -f compose.prod.yml exec web python manage.py createsuperuser
```

- `web`: imagen multi-stage (build de producción de webpack + Python), gunicorn con usuario no-root. `migrate` y `collectstatic` se ejecutan en cada arranque.
- `nginx`: escucha en el puerto 80 (se cambia con `HTTP_PORT`), sirve `/static/` y `/media/` y pasa el resto a gunicorn.
- `db`: PostgreSQL con los datos en el volumen `pgdata`. Los archivos subidos van al volumen `media`. Haz copias de seguridad de los dos.
- HTTPS no está incluido: hay que terminar TLS delante de este stack (nginx del host + certbot, Caddy, Traefik o el balanceador del proveedor). Guía paso a paso con nginx del host + certbot: [2_DEPLOYMENT.md](manuals/ES/2_DEPLOYMENT.md). Pon `HTTP_PORT=127.0.0.1:8080` para que el stack solo sea accesible a través de ese proxy.

Para actualizar: `git pull && docker compose -f compose.prod.yml up -d --build`.

## Configuración (`.env`)

| Variable | Dev | Prod | Notas |
|---|---|---|---|
| `SECRET_KEY` | opcional | **obligatoria** | `docker compose run --rm web python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `POSTGRES_DB` / `POSTGRES_USER` / `POSTGRES_PASSWORD` | opcional | **obligatoria** | Las usa el contenedor `db` y sirven para construir `DATABASE_URL`. Evita `@ : / ? #` en la contraseña. |
| `ALLOWED_HOSTS` | opcional | **obligatoria** | Separadas por comas |
| `CSRF_TRUSTED_ORIGINS` | – | recomendada | p. ej. `https://example.com,https://www.example.com` |
| `SECURE_HTTPS` | – | opcional | Por defecto `True`: redirección a HTTPS + cookies seguras. Ponerla a `False` solo para probar el stack de prod por HTTP. |
| `SECURE_HSTS_SECONDS` | – | opcional | Por defecto `0`. Empezar con `3600` y subir a `31536000` cuando HTTPS esté confirmado. |
| `WEB_PORT` / `HTTP_PORT` | opcional | opcional | Puertos del host (dev: 8000, prod: 80) |
| `DATABASE_URL` | – | – | La pone compose. Solo hace falta si ejecutas Django fuera de Docker. |

Nunca subas el `.env` al repo.
