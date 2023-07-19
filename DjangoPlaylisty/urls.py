from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("auth/", views.auth, name="auth"),
    path("callback/", views.callback, name="callback"),
    path("logout/", views.logout, name="logout"),
    path("createplaylist/", views.create_playlist, name="createplaylist"),
    path("getplaylist/", views.get_playlist, name="getplaylist"),
    path(
        "createplaylist/getitem/<str:item_str>/<str:item_type>",
        views.get_item,
        name="getitem",
    ),
    path("generatedplaylist/", views.generated_playlist, name="generatedplaylist"),
    path("ups/", views.not_white_listed, name="notwhitelisted"),
    path("whylogin/", views.why_login, name="whylogin"),
    path('getloginstatus/', views.get_login_status, name='getloginstatus'),
]
