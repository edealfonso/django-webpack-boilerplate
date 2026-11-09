# Deployment en un servidor (VPS) con Docker

Este stack (`compose.prod.yml`) levanta **nginx + gunicorn + Postgres**. HTTPS se pone delante con el nginx del propio servidor y certbot (Let's Encrypt).

```
Internet ──443──> nginx del host (TLS, certbot) ──> 127.0.0.1:8080 ──> nginx (contenedor) ──> gunicorn
```

## 0. Preparar el servidor

Entrar y actualizar (Ubuntu/Debian):

```bash
ssh root@__ip__
apt update && apt upgrade -y
```

Recomendado: entrar con clave SSH en vez de contraseña:

```bash
ssh-copy-id root@__ip__      # desde tu ordenador
```

Instalar Docker (incluye Compose): https://docs.docker.com/engine/install/ubuntu/ (o `curl -fsSL https://get.docker.com | sh`).

## 1. Clonar el proyecto

```bash
mkdir -p /webapps && cd /webapps
git clone __repositorio__ __proyecto__
cd __proyecto__/__carpeta_django__        # donde están compose.prod.yml y .env.example
```

Para un repo privado, hay que crear antes una deploy key (`ssh-keygen -t ed25519`) y añadirla en GitHub/GitLab.

## 2. Configurar `.env`

```bash
cp .env.example .env
nano .env
```

Valores mínimos:

```bash
SECRET_KEY=__clave_larga_y_aleatoria__
POSTGRES_DB=__proyecto__
POSTGRES_USER=__proyecto__
POSTGRES_PASSWORD=__contraseña_sin_@:/?#__
ALLOWED_HOSTS=__dominio__,www.__dominio__
CSRF_TRUSTED_ORIGINS=https://__dominio__,https://www.__dominio__
HTTP_PORT=127.0.0.1:8080      # solo accesible desde el propio servidor (el nginx del host)
```

Generar la `SECRET_KEY`:

```bash
docker run --rm python:3.13-slim python -c "import secrets; print(secrets.token_urlsafe(50))"
```

## 3. Arrancar

```bash
docker compose -f compose.prod.yml up -d --build
docker compose -f compose.prod.yml exec web python manage.py createsuperuser
```

`migrate` y `collectstatic` se ejecutan solos en cada arranque.

Si tienes un dump de la base de datos, mira [BASES_DE_DATOS_POSTGRES.md](BASES_DE_DATOS_POSTGRES.md) para restaurarlo (con `-f compose.prod.yml`).

## 4. HTTPS con nginx del host + certbot

```bash
apt install -y nginx certbot python3-certbot-nginx
```

Crear `/etc/nginx/sites-available/__proyecto__`:

```nginx
server {
    listen 80;
    server_name __dominio__ www.__dominio__;

    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Activarlo y pedir el certificado (el DNS del dominio ya tiene que apuntar al servidor):

```bash
ln -s /etc/nginx/sites-available/__proyecto__ /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
certbot --nginx -d __dominio__ -d www.__dominio__
```

certbot añade el bloque 443, la redirección y la renovación automática.

Cuando todo vaya por HTTPS, se puede activar HSTS poniendo en `.env` `SECURE_HSTS_SECONDS=3600` (y más adelante `31536000`) y reiniciando: `docker compose -f compose.prod.yml up -d`.

> Varios proyectos en el mismo servidor: cada uno con su `HTTP_PORT` (`127.0.0.1:8080`, `127.0.0.1:8081`...) y su archivo en `sites-available`.

## Actualizar

```bash
cd /webapps/__proyecto__/__carpeta_django__
git pull
docker compose -f compose.prod.yml up -d --build
```

## Comandos útiles

```bash
docker compose -f compose.prod.yml ps                 # estado
docker compose -f compose.prod.yml logs -f web        # logs de Django/gunicorn
docker compose -f compose.prod.yml logs -f nginx
docker compose -f compose.prod.yml restart web
docker compose -f compose.prod.yml exec web python manage.py shell
```

Los contenedores tienen `restart: unless-stopped`: vuelven a arrancar solos si se reinicia el servidor.

## Copias de seguridad

Los datos están en volúmenes de Docker: `pgdata` (base de datos) y `media` (archivos subidos).

- Base de datos: ver [BASES_DE_DATOS_POSTGRES.md](BASES_DE_DATOS_POSTGRES.md).
- Media:
  ```bash
  docker compose -f compose.prod.yml cp web:/app/media ./media-backup
  ```
