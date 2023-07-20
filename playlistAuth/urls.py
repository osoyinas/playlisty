from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("auth/", views.auth, name="auth"),
    path("callback/", views.callback, name="callback"),
    path("logout/", views.logout, name="logout"),
    path('getloginstatus/', views.get_login_status, name='getloginstatus'),
]
