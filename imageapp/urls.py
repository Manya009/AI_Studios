from django.urls import path
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("image_generate/", views.image_generator, name="image_generator"),
]