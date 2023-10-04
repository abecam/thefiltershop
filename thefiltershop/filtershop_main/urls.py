from django.urls import path

from . import views
from .admin import admin_site

app_name = "filtershop_games"
urlpatterns = [
    path("", views.index, name="index"),
    path("index", views.index, name="index"),
    path("<int:videogame_id>/", views.game, name="game"),
    path("index_online_shops", views.index_online_shops, name="index_online_shops"),
    path("online_shop/<int:shop_id>/", views.online_shop, name="online_shop"),
    path("artisans_games", views.get_artisans_games, name="artisans_games"),
    path("indies_games", views.get_indies_games, name="indies_games"),
    path("curators", views.get_curators, name="curators"),
    #path('admin/', admin_site.urls),
]