# Bases de datos (Postgres en Docker)

Postgres corre en el servicio `db`. El usuario y la base de datos salen de `POSTGRES_USER` / `POSTGRES_DB` (`.env`, o `myproject` por defecto en desarrollo). Los comandos usan esas variables desde dentro del contenedor, así que no hace falta escribirlas.

Todos los comandos se ejecutan desde la carpeta del proyecto. **En producción** hay que añadir `-f compose.prod.yml` después de `docker compose`.

## Consola SQL (psql)

```bash
docker compose exec db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
```

## Crear dump

```bash
docker compose exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB"' > __nombre_dump__.sql
```

El archivo se crea en tu carpeta actual (fuera del contenedor).

## Restaurar un dump

Lo más limpio es restaurar sobre una base de datos vacía:

```bash
# 1. Vaciar la base de datos (BORRA todos los datos)
docker compose stop web
docker compose exec db sh -c 'dropdb -U "$POSTGRES_USER" --force "$POSTGRES_DB" && createdb -U "$POSTGRES_USER" "$POSTGRES_DB"'

# 2. Cargar el dump
docker compose exec -T db sh -c 'psql -q -U "$POSTGRES_USER" -d "$POSTGRES_DB"' < __nombre_dump__.sql

# 3. Volver a arrancar (y migrar si el dump es de una versión anterior del código)
docker compose start web
docker compose exec web python manage.py migrate
```

- Si el dump viene de otra base de datos con otro usuario propietario, añade `--no-owner --no-privileges` al hacer el `pg_dump`, o ignora los errores de `ALTER ... OWNER` al restaurar.

## Borrar la base de datos entera

```bash
docker compose down -v      # borra los volúmenes: base de datos (y node_modules en dev)
```

En producción `down -v` también borra `media` y `staticfiles`. Si solo quieres vaciar la base de datos, usa el paso 1 de "Restaurar un dump".

## Conectar un cliente de BD (TablePlus, DBeaver, pgAdmin...)

En desarrollo, descomentar `ports` en el servicio `db` de `compose.yml` y reiniciar (`docker compose up -d`). Después conectar a `localhost:5432` (o `DB_PORT`) con el usuario y la contraseña de `.env`.

## Otras cosas útiles

### Importar desde un CSV a la DB

Copiar el CSV dentro del contenedor:

```bash
docker compose cp Libro2.csv db:/tmp/Libro2.csv
```

Y desde la consola SQL (ver arriba):

```sql
COPY art_auximg
FROM '/tmp/Libro2.csv'
DELIMITER ',' CSV HEADER;
```

La última línea describe el delimitador y si hay cabecera. Por ejemplo, el script de arriba funcionaría con este CSV:

```csv
id,num
11,0
12,1
13,2
```

### Modificar toda una columna con valores de la columna de otra tabla

```sql
UPDATE tabla_destino
SET    "columna_destino" = tabla_origen.columna_origen
FROM   tabla_origen
WHERE  tabla_origen.id = tabla_destino.id;
```

## Ref

- Imagen oficial de Postgres: https://hub.docker.com/_/postgres
- pg_dump: https://www.postgresql.org/docs/current/app-pgdump.html
