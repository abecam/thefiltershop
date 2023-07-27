from django.urls import path

from . import views
from .admin import admin_site

app_name = "filtershop_games"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:videogame_id>/", views.game, name="game"),
    #path('admin/', admin_site.urls),
]