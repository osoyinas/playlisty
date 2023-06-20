"""DjangoPlaylisty URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name= 'home'),
    path('auth/', views.auth, name='auth'),
    path('callback/', views.callback, name = 'callback'),
    path('logout/', views.logout, name = 'logout'),
    path('createplaylist/', views.create_playlist, name = 'createplaylist'),
    path('getplaylist/', views.get_playlist, name = 'getplaylist'),
    path('createplaylist/getitem/<str:item_str>/<str:item_type>', views.get_item, name = 'getitem'),
    path('getloginstatus/', views.getLoginStatus, name='getloginstatus')
]
