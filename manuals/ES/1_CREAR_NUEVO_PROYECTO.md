## Crear entorno

```
python3 -m venv __nombreentorno__
source __nombreentorno__/bin/activate
pip3 install django
```

## VIA 1: Copiar esta plantilla

Copiar plantilla, cambiar la palabra "elsas-project" por el nombre de tu proyecto en todos los archivos.

Generar clave secreta nueva para secret.json: https://djecrety.ir/

## VIA 2: Crear proyecto y apps desde cero

El proyecto se crea así:
```
django-admin startproject __nombreproyecto__
```
Las apps así:
```
django-admin startapp __nombreapp__
```
Luego hay que añadirla a INSTALLED_APPS en settings.base.


## Crear DB
- Si nunca usaste postgres instalar y configurar **en MacOSX** así:
```bash
brew install postgres
brew services start postgres
/usr/local/opt/postgres/bin/createuser -s postgres
````

- Crear db y usuario + entrar en base de datos
```
sudo su postgres [+ introducir contraseña user]
createdb __nombre_db__ [+ introducir contraseña psql]
```

## Cambiar permisos DB (opcional)
A veces es necesario hacer esto después de crear la DB.
```
createuser __nombre_user__
psql __nombre_db__
```
- Otorgar derechos a user
```
alter user __nombre_user__ with password '__pass__';
exit
exit
```
## errores de unipath para las versiones (4.*.*) de Django (reemplazar)
```
    myenv\Lib\site-packages\adminsortable\admin.py
        from django.conf.urls import re_path -> from django.urls import re_path as url
```

## Migración de los modelos a la base de datos
```
    python3 manage.py migrate
```

## Crear usuario y arrancar servidor
```
python3 manage.py createsuperuser
python3 manage.py runserver
```
