# Cambiar política de caché

1. Cambiar esta parte del archivo de `sites-available`:
```bash
    location /static/ {
        alias   /webapps/unfinished/unfinished/staticfiles/;
        expires 365d;
    }
    
    location /media/ {
        alias   /webapps/unfinished/unfinished/media/;
        expires 30d;
    }
``` 
2. Volver a crear el link simbólico y reiniciar
```bash
ln -s /etc/nginx/sites-available/__proyecto__ /etc/nginx/sites-enabled/__proyecto__
service nginx restart

````
3. Si se van a hacer cambios en `staticfiles` a lo mejor hay que resetear (borrar carpeta caché + restart) **????**

