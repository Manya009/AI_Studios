from django.urls import path
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="hello"),
    path("story_predict/", views.story_predictor, name="story_predictor"),
]
