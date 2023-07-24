"""
Django project urls.

"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("createplaylist/", include('playlistGeneration.urls'), name='createplaylist'),
    path("", include('playlistAuth.urls')),
    path("whylogin/", views.why_login, name="whylogin"),
    path("ups/", views.not_white_listed, name="notwhitelisted"),
]
