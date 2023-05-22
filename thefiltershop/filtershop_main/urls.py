from django.urls import path

from . import views

app_name = "filtershop_games"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:videogame_id>/", views.game, name="game"),
]