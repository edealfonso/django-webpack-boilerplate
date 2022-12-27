from django.urls import path

from .views import *

app_name = 'pages_app'

urlpatterns = [
    path('', LandingView.as_view(), name="landing"),
    # path('salut-mental', HomeArtView.as_view(), name="salut-mental"),
    # path('histories', HomeArtView.as_view(), name="histories"),
    # path('parlar', HomeArtView.as_view(), name="parlar"),
    # path('ajuda', HomeArtView.as_view(), name="ajuda"),
]
