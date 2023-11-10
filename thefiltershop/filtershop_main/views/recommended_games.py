from django.shortcuts import render
from django.db.models import Q
from django.db.models import Count
from django.core.paginator import Paginator

from ..models import Videogame_common, Game_Category, Studio, Publisher

def get_recommended_games(request):
    game_categories = Game_Category.objects.all()
    recommender = request.GET.get('from')
    category_id = request.GET.get('category_id')  # Get the selected category ID from the query parameters
    page_number = request.GET.get("page")

    # Get all artisan games
    list_of_games_artisan = get_all_games_for_size(Studio.SizeInPersons.ARTISAN)

    # Apply category filtering if a category is selected
    if category_id:
        list_of_games_artisan = list_of_games_artisan.filter(categories__id=category_id)

    paginator = Paginator(list_of_games_artisan, 8)  

    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "categories": game_categories, "selected_category": category_id}

    return render(request, "thefiltershop/artisans_games.html", context)

def get_all_games_for_size(max_size_of_studio) :
    if not isinstance(max_size_of_studio, Studio.SizeInPersons):
        raise TypeError('max_size_of_studio_or_publisher must be a Studio_and_Publisher_Size')
    
    if max_size_of_studio != Studio.SizeInPersons.ARTISAN :
        # No filter on publisher size for non-artisan
        all_for_size = Videogame_common.objects.filter(studios__size_of_studio = max_size_of_studio).order_by("known_popularity")
    else :
        all_for_size = Videogame_common.objects.filter(studios__size_of_studio = Studio.SizeInPersons.ARTISAN, publishers__size_of_publisher = Publisher.SizeInPersons.ARTISAN).order_by("known_popularity")
    
    return all_for_size