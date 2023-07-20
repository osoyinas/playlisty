from django.urls import path
from . import views


urlpatterns = [
    path("", views.create_playlist, name="createplaylist"),
    path("getplaylist/", views.get_playlist, name="getplaylist"),
    path(
        "getitem/<str:item_str>/<str:item_type>",
        views.get_item,
        name="getitem",
    ),
    path("generatedplaylist/", views.generated_playlist, name="generatedplaylist"),
]
