from django.urls import path

from . import views
from .admin import admin_site
from django.views.generic import TemplateView

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
    path("all_filters", views.get_all_filters, name="all_filters"),
    path("game_filters", views.get_all_filters_for_an_entity_type_videogame, name="game_filters"),
    path("one_filter/<int:filter_id>/", views.get_one_filter_and_related_filters, name="one_filter"),
    path("they_made_it", views.get_artisans_and_indies_games_that_made_it, name="they_made_it"),
    path("hall_of_shame", views.get_items_in_hall_of_shame, name="hall_of_shame"),
    path("physical_shop/<int:shop_id>/", views.physical_shop, name="physical_shop"),
    path("index_physical_shops", views.index_physical_shops, name="index_physical_shops"),
    path("our_mission", TemplateView.as_view(template_name="thefiltershop/our_mission.html"), name="our_mission"),
    path("who_are_we", TemplateView.as_view(template_name="thefiltershop/who_are_we.html"), name="who_are_we"),
    path("our_sponsors", views.get_sponsors, name="our_sponsors"),
    path("online_artisans_shops", views.get_artisans_online_shops, name="online_artisans_shops"),
    path("online_indies_shops", views.get_indies_online_shops, name="online_indies_shops"),
    path("online_other_shops", views.get_others_online_shops, name="online_other_shops"),
    path("they_made_it_online_shops", views.get_artisans_and_indies_shops_that_made_it, name="they_made_it_online_shops"),
    path("online_shop_filters", views.get_all_filters_for_an_entity_type_online_shop, name="online_shop_filters"),
    #path('admin/', admin_site.urls),
]