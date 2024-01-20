from django.urls import path, include
from . import views

urlpatterns = [
    path("movie_generate/", views.movie, name="movie")

]