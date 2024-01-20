from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("images_gallery/", views.homie, name="story")
]
