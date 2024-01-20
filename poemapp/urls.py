from django.urls import path
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("poem_predict/", views.poem_predictor, name="story_predictor"),
]
