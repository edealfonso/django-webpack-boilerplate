# Crear un proyecto nuevo

Solo hace falta [Docker](https://docs.docker.com/get-docker/). Python, Node y Postgres van dentro de los contenedores.

## 1. Copiar la plantilla

```bash
git clone git@github.com:edealfonso/django-webpack-boilerplate.git __nombreproyecto__
cd __nombreproyecto__
rm -rf .git && git init
```

Cambiar `myproject` por el nombre del proyecto en todas partes:

- La carpeta `myproject/`
- `package.json` (`name`)
- Los valores por defecto de `compose.yml` (`POSTGRES_DB`, `POSTGRES_USER`...) y de `.env.example`
- Los títulos del admin en `config/urls.py`
- La plantilla `templates/home.html`

Para encontrar todas las apariciones: `grep -rn myproject --exclude-dir=node_modules --exclude=package-lock.json .`

## 2. Arrancar

```bash
cd __nombreproyecto__        # la carpeta que antes era myproject/
docker compose up --build
```

En otra terminal:

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

- Web: http://localhost:8000. Admin: http://localhost:8000/admin/
- La primera vez hay que esperar a que webpack termine (`docker compose logs -f assets`). Si no, la página da error porque todavía no existe `webpack-stats.json`.
- En desarrollo no hace falta `.env`: todas las variables tienen valor por defecto. Si quieres cambiar alguna, copia `.env.example` a `.env`.

## 3. Crear una app

Las apps van dentro de `apps/`:

```bash
docker compose exec web sh -c "mkdir -p apps/__nombreapp__ && python manage.py startapp __nombreapp__ apps/__nombreapp__"
```

Después:

1. En `apps/__nombreapp__/apps.py` cambiar `name = '__nombreapp__'` por `name = 'apps.__nombreapp__'`.
2. Añadir `'apps.__nombreapp__'` a `LOCAL_APPS` en `config/settings/base.py`.
3. Si tiene urls, crear `apps/__nombreapp__/urls.py` (con `app_name = '__nombreapp___app'`) e incluirlo en `config/urls.py`.

En `apps/pages` y `apps/content` hay un ejemplo comentado de modelo y admin con el editor de texto (`ProseEditorField`) y el orden por arrastre (`SortableAdminMixin`).

## 4. Modelos y migraciones

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

## 5. Dependencias

- **Python**: añadirla a `requirements.txt` y reconstruir: `docker compose build web && docker compose up -d`
- **JS/CSS**: `docker compose run --rm assets npm install __paquete__`

## Parar y limpiar

```bash
docker compose down        # para los contenedores (los datos se conservan)
docker compose down -v     # para y BORRA la base de datos y node_modules
```
