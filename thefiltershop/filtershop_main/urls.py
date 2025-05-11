from django.urls import path

from . import views
from .admin import admin_site
from django.views.generic import TemplateView

app_name = "filtershop_games"
urlpatterns = [
    path("", views.index, name="index"),
    path("index", views.index, name="index"),
    path("<int:videogame_id>/", views.game, name="game"),
    path("studio/<int:studio_id>/", views.studio, name="studio"),
    path("publisher/<int:publisher_id>/", views.publisher, name="publisher"),
    path("artisans_games", views.get_artisans_games, name="artisans_games"),
    path("indies_games", views.get_indies_games, name="indies_games"),
    path("curators", views.get_curators, name="curators"),
    path("all_filters", views.get_all_filters, name="all_filters"),
    path("game_filters", views.get_all_filters_for_an_entity_type_videogame, name="game_filters"),
    path("one_filter/<int:filter_id>/", views.get_one_filter_and_related_filters, name="one_filter"),
    path("they_made_it", views.get_artisans_and_indies_games_that_made_it, name="they_made_it"),
    path("best_of_the_rest", views.get_best_of_the_rest, name="best_of_the_rest"),
    path("hall_of_shame", views.get_items_in_hall_of_shame, name="hall_of_shame"),
    path("our_mission", TemplateView.as_view(template_name="thefiltershop/our_mission.html"), name="our_mission"),
    path("who_are_we", TemplateView.as_view(template_name="thefiltershop/who_are_we.html"), name="who_are_we"),
    path("our_sponsors", views.get_sponsors, name="our_sponsors"),
    path("a_random_artisan_game", views.get_a_random_unfiltered_artisan_game, name="a_random_artisan_game"),
    path("a_random_indie_game", views.get_a_random_unfiltered_indie_game, name="a_random_indie_game"),
    path("videogames_search/", views.get_search_results, name="videogames_search"),
    path("four_o_four", TemplateView.as_view(template_name="404.html"), name="404"),
    path("a_random_recommender", views.get_a_random_contributor, name="a_random_recommender"),
    path("a_recommender", views.get_recommended_games, name="a_recommender")
    #path('admin/', admin_site.urls),
]