from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sections/<int:num>", views.section, name="section"),
]
