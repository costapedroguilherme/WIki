from django.urls import path

from . import views
from . import util

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.wiki, name="wiki"),
]
