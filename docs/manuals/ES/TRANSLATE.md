# Traducciones

Dos partes independientes:

- **Contenido estático** (textos de las plantillas y del código): i18n de Django, con `makemessages` / `compilemessages`.
- **Contenido dinámico** (campos de los modelos): [django-modeltranslation](https://django-modeltranslation.readthedocs.io/).

## 0. Preparar la imagen: gettext

`makemessages` y `compilemessages` necesitan GNU gettext, que no viene en la imagen `python:slim`. Añadirlo en el stage `base` del `Dockerfile`, antes del `pip install`:

```dockerfile
RUN apt-get update \
    && apt-get install -y --no-install-recommends gettext \
    && rm -rf /var/lib/apt/lists/*
```

Y reconstruir: `docker compose build web && docker compose up -d`.

## 1. Settings

En `config/settings/base.py`, apartado *Internationalization*:

```py
# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es'

LANGUAGES = [
    ('es', 'Español'),
    ('en', 'English'),
]

LOCALE_PATHS = [BASE_DIR / 'locale']

TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
```

Añadir el middleware **después** de `SessionMiddleware` y **antes** de `CommonMiddleware`:

```py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    # ...
]
```

## 2. URLs con prefijo de idioma

`config/urls.py`:

```py
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # vista set_language (opcional)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('apps.pages.urls')),
    path('', include('apps.content.urls')),
    prefix_default_language=True,
)
```

## 3. Contenido estático

1. En las plantillas: `{% load i18n %}` y `{% translate "..." %}` (o `{% blocktranslate %}...{% endblocktranslate %}`). En Python: `from django.utils.translation import gettext_lazy as _` y `_("...")`.
2. Crear la carpeta `locale/` en la raíz del proyecto (`mkdir locale`).
3. Generar los archivos de traducción (uno por idioma):
   ```bash
   docker compose exec web python manage.py makemessages -l en --ignore=node_modules
   ```
4. Rellenar `locale/en/LC_MESSAGES/django.po`.
5. Compilar:
   ```bash
   docker compose exec web python manage.py compilemessages --ignore=node_modules
   ```

Los `.po` y los `.mo` se suben al repo (en producción no se ejecuta `compilemessages`).

## 4. Contenido dinámico: django-modeltranslation

1. Añadir `django-modeltranslation` a `requirements.txt` y reconstruir (`docker compose build web`).
2. Añadir `'modeltranslation'` a `INSTALLED_APPS` **antes** de `'django.contrib.admin'`. Como `THIRD_PARTY_APPS` va primero en `base.py`, basta con descomentarlo ahí.
3. Crear `translation.py` en la app con los campos a traducir ([docs](https://django-modeltranslation.readthedocs.io/en/latest/registration.html)):
    ```py
    from modeltranslation.translator import TranslationOptions, register

    from .models import LegalPage


    @register(LegalPage)
    class LegalPageTranslationOptions(TranslationOptions):
        fields = ('title', 'text')
    ```
4. Los admins tienen que heredar de `TranslationAdmin`. Si hay otros mixins (como `SortableAdminMixin`), los mixins van delante:
    ```py
    from adminsortable2.admin import SortableAdminMixin
    from modeltranslation.admin import TranslationAdmin


    @admin.register(LegalPage)
    class LegalPageAdmin(SortableAdminMixin, TranslationAdmin):
        pass
    ```
5. Migrar para crear los campos de cada idioma (`title_es`, `title_en`...):
    ```bash
    docker compose exec web python manage.py makemigrations
    docker compose exec web python manage.py migrate
    ```
6. Si traduces campos que ya tenían datos, copia el valor existente al idioma por defecto ([docs](https://django-modeltranslation.readthedocs.io/en/latest/commands.html)):
    ```bash
    docker compose exec web python manage.py update_translation_fields
    # o solo una app/modelo e idioma:
    docker compose exec web python manage.py update_translation_fields __myapp__ __mymodel__ --language en
    ```

## 5. Selector de idioma

Enlace simple que cambia el prefijo de la URL:

```html
{% load i18n %}
{% get_current_language as LANGUAGE_CODE %}
{% if LANGUAGE_CODE == "en" %}
<a href="/es{{ request.get_full_path|slice:'3:' }}">ES</a>
{% else %}
<a href="/en{{ request.get_full_path|slice:'3:' }}">EN</a>
{% endif %}
```

Alternativa con la vista `set_language` de Django (recuerda el idioma en una cookie): https://docs.djangoproject.com/en/5.2/topics/i18n/translation/#the-set-language-redirect-view
