## Crear dump
En general debería funcionar:
```bash
su postgres
pg_dump __nombre_db__ > __nombre_dump__.sql
```
- Si da problemas de permisos es porque en la carpeta en la que estás el usuario postgres no tiene permiso para crear el archivo de dump. 
- A veces hay que cambiar de directorio `cd ..` porque se coloca en uno raro al hacer `su postgres`.
- Ejemplo en server:
    ```bash
    su postgres
    cd ..
    pg_dump __nombre_db__ > /tmp/__nombre_dump__.sql
    ```

En macOSX funciona:
```bash
sudo su postgres [+ introducir contraseña user Mac]
pg_dump __nombre_db__ > /tmp/__nombre_dump__.sql [+ introducir contraseña pgadmin ]
```
Entonces tendremos el dump en el directorio `/tmp`.


## Modificar/restablecer DB a partir de un dump

Poner el dump (archivo .sql) en el directorio raíz (o en otro y poner el path abajo).

Abrir terminal y poner estos comandos:
```bash
sudo -i
su - postgres
cd /
psql __nombre_db__ < __nombre_dump__.sql
```
Notas:
- Si te da problemas de permisos, se tendrán que dar a los archivos sql permisos de acceso/ejecución a todes.

**Alternativa nueva**
Me ha funcionado esto, copiando el dump en el root del server:
```bash
chmod a+r /__nombre_dump__.sql
su postgres
psql __nombre_db__ < __nombre_dump__.sql
```

## Cambiar admin de una DB
```bash
su postgres
CREATE USER qfactoryuser WITH PASSWORD 'xxxxx';
psql qfactory -c "GRANT ALL ON ALL TABLES IN SCHEMA public to qfactoryuser;"
psql qfactory -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA public to qfactoryuser;"
psql qfactory -c "GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to qfactoryuser;"
exit
```


## Otras cosas complicadas

### Importar desde un CSV a la DB

```sql
COPY art_auximg
FROM '/Libro2.csv'
DELIMITER ',' CSV HEADER;
```
En esta última línea se describe el delimitador y si hay header o no. Por ejemplo el script de arriba funcionaría bien con este CSV:
```csv
id,num
11,0
12,1
13,2
14,7
15,1
16,2
17,3
```

### Modificar toda una columna con valores de la columna de otra tabla
```sql
UPDATE tabla_destino 
SET    "columna_destino" = tabla_origen.columna_origen
FROM   tabla_origen 
WHERE  tabla_origen.id = tabla_destino.id;
```


### Borrar DB
```bash
sudo su postgres [+ introducir contraseña user]
dropdb __nombre_db__
```

## Ref
- Importar y exportar DB: 
https://www.a2hosting.com/kb/developer-corner/postgresql/import-and-export-a-postgresql-database

