from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator

from ..models import Videogame_common, Game_Category, Studio, Publisher

def get_artisans_games(request):
    game_categories = Game_Category.objects.all()
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


def get_indies_games(request):
    list_of_games_indies = get_all_games_for_size(Studio.SizeInPersons.INDIE)

    paginator = Paginator(list_of_games_indies, 25)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}

    return render(request, "thefiltershop/indies_games.html", context)

def get_artisans_and_indies_games_that_made_it(request):
    list_of_games_that_made_it = get_all_games_that_made_it()

    paginator = Paginator(list_of_games_that_made_it, 25)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    
    return render(request, "thefiltershop/they_made_it.html", context)

def get_all_games_for_size(max_size_of_studio) :
    if not isinstance(max_size_of_studio, Studio.SizeInPersons):
        raise TypeError('max_size_of_studio_or_publisher must be a Studio_and_Publisher_Size')
    
    if max_size_of_studio != Studio.SizeInPersons.ARTISAN :
        # No filter on publisher size for non-artisan
        all_for_size = Videogame_common.objects.filter(studios__size_of_studio = max_size_of_studio)
    else :
        all_for_size = Videogame_common.objects.filter(studios__size_of_studio = Studio.SizeInPersons.ARTISAN, publishers__size_of_publisher = Publisher.SizeInPersons.ARTISAN)
    
    return all_for_size

def get_all_games_that_made_it() :
    # Here we don't care about the Publisher size
    all_for_size = Videogame_common.objects.filter(Q(studios__size_of_studio =  Studio.SizeInPersons.ARTISAN) | Q(studios__size_of_studio =  Studio.SizeInPersons.INDIE), they_have_made_it__gt = 0)
    
    return all_for_size