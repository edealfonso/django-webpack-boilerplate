# Translate

## Instalación

0. Instalar pip: `pip install django-modeltranslation` ([docs](https://django-modeltranslation.readthedocs.io/en/latest/installation.html))
1. Add `modeltranslation` to the `INSTALLED_APPS` variable of your project’s `settings.py`
2. Cambiar el apartado de *Internationalization* en `settings.py`:
    ```py
    # Internationalization
    # https://docs.djangoproject.com/en/3.2/topics/i18n/

    LANGUAGE_CODE = 'es'

    LANGUAGES = (
        ('es', 'Spanish'),
        ('en', 'English'),
    )

    # Static data translate
    LOCALE_PATHS = (
        os.path.join(BASE_DIR, 'locale'),
    )

    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    ```

## Incorporar traducciones en el contenido dinámico

1. Crear `translation.py` especificando los campos a traducir ([docs](https://django-modeltranslation.readthedocs.io/en/latest/registration.html?highlight=TranslationOptions)). 

    Ejemplo:
    ```py
    from modeltranslation.translator import translator, TranslationOptions
    from .models import *

    class LegalPageTranslationOptions(TranslationOptions):
        fields = ( 'title', 'text')
    translator.register(LegalPage, LegalPageTranslationOptions)
    ```

2. Sus correspondientes admins han de ser `TranslationAdmin`. En caso de tener varias clases se pone siempre al final:

    ```py
    class LegalPageAdmin(SortableAdmin, TranslationAdmin):
        pass
    admin.site.register(LegalPage, LegalPageAdmin)
    ```
    
3. Migrar para que se generen los campos de las traducciones en la DB

4. Si se decide traducir campos ya existentes y rellenados en la base de datos, se pueden duplicar traducciones ([docs](https://django-modeltranslation.readthedocs.io/en/latest/commands.html)) mediante el comando `python manage.py update_translation_fields`. Se puede espeficiar app, modelo, y campo al que quieres que vaya a parar la info así: `python manage.py update_translation_fields __myapp__ __mymodel__ --language en`.

5. Añadir *middleware* en `settings.py`:
    ```py
    MIDDLEWARE = [
        #...
        'django.middleware.locale.LocaleMiddleware',
    ]
    ```

6. Cambiar el archivo `urls.py` general, tal que así:
    ```py
    """qfactory URL Configuration
    """
    from django.contrib import admin
    from django.urls import path, include, re_path

    from django.conf import settings
    from django.conf.urls.static import static
    from django.conf.urls.i18n import i18n_patterns


    urlpatterns = [

    ]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

    urlpatterns += i18n_patterns (
        path('admin/', admin.site.urls),

        # include apps urls
        re_path('', include('apps.pages.urls', namespace='pages__app')),
        re_path('', include('apps.galerias.urls', namespace='galerias_app')),

        # path('__debug__/', include('debug_toolbar.urls')),

        prefix_default_language=True,
    )

    # Title change
    admin.site.site_header = "QFACTORY"
    admin.site.index_title = "Administrador de contenidos"
    admin.site.site_title = "QFACTORY"
    ```

7. Para poner los selectores de idioma, se pone esto:
    ```html
    {% get_current_language as LANGUAGE_CODE %}
    {% if LANGUAGE_CODE == "en" %}
    <a class="header__menu__nav__item--lang" href="/es{{ request.get_full_path|slice:'3:' }}">ES</a>
    {% else %}
    <a class="header__menu__nav__item--lang" href="/en{{ request.get_full_path|slice:'3:' }}">EN</a>
    {% endif %}
    ```



## Incorporar traducciones en el contenido estático

3. En las templates poner todo como `{% trans '....' %}` (o `blocktranslate`)
4. Ejecutar `python manage.py makemessages -l en` (cambiar `en` por el código de cada idioma al que traduces)
5. Rellenar archivos editables creados en `locale`
6. Ejecutar `python manage.py compilemessages`


