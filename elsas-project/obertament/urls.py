"""elsas-project URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # include apps urls
    path('', include('apps.pages.urls')),
    path('', include('apps.content.urls')),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


# Title change
admin.site.site_header = "elsas-project"
admin.site.index_title = "Back-End Admin"
admin.site.site_title = "elsas-project"