import random
from django.shortcuts import render
from django.db.models import Q
from django.db.models import Count
from django.core.paginator import Paginator

from .view_a_game import game

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
    selected_category_name = Game_Category.objects.filter(id=category_id).values_list('name', flat=True).first() if category_id else None

    context = {"page_obj": page_obj, "categories": game_categories, "selected_category": category_id, "selected_category_name": selected_category_name}

    return render(request, "thefiltershop/artisans_games.html", context)


def get_indies_games(request):
    game_categories = Game_Category.objects.all()
    category_id = request.GET.get('category_id')  # Get the selected category ID from the query parameters
    
    list_of_games_indies = get_all_games_for_size(Studio.SizeInPersons.INDIE)

    # Apply category filtering if a category is selected
    if category_id:
        list_of_games_indies = list_of_games_indies.filter(categories__id=category_id)
        
    paginator = Paginator(list_of_games_indies, 8)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    selected_category_name = Game_Category.objects.filter(id=category_id).values_list('name', flat=True).first() if category_id else None

    context = {"page_obj": page_obj, "categories": game_categories, "selected_category": category_id, "selected_category_name": selected_category_name}

    return render(request, "thefiltershop/indies_games.html", context)

def get_artisans_and_indies_games_that_made_it(request):
    game_categories = Game_Category.objects.all()
    category_id = request.GET.get('category_id')  # Get the selected category ID from the query parameters
    
    list_of_games_that_made_it = get_all_games_that_made_it()
    
    # Apply category filtering if a category is selected
    if category_id:
        list_of_games_that_made_it = list_of_games_that_made_it.filter(categories__id=category_id)

    paginator = Paginator(list_of_games_that_made_it, 25)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    selected_category_name = Game_Category.objects.filter(id=category_id).values_list('name', flat=True).first() if category_id else None

    context = {"page_obj": page_obj, "categories": game_categories, "selected_category": category_id, "selected_category_name": selected_category_name}
    
    return render(request, "thefiltershop/they_made_it.html", context)

def get_best_of_the_rest(request):
    game_categories = Game_Category.objects.all()
    category_id = request.GET.get('category_id')  # Get the selected category ID from the query parameters
    
    # get_all_best_of_the_rest return a list, so the filtering for category needs to be done before.
    list_of_best_of_the_rest = get_all_games_for_size(Studio.SizeInPersons.MEDIUM) | get_all_games_for_size(Studio.SizeInPersons.BIG) | get_all_games_for_size(Studio.SizeInPersons.HUGE)
        
    paginator = Paginator(list_of_best_of_the_rest, 25)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    selected_category_name = Game_Category.objects.filter(id=category_id).values_list('name', flat=True).first() if category_id else None

    context = {"page_obj": page_obj, "categories": game_categories, "selected_category": category_id, "selected_category_name": selected_category_name}

    return render(request, "thefiltershop/best_of_the_rest.html", context)

def get_all_games_for_size(max_size_of_studio) :
    if not isinstance(max_size_of_studio, Studio.SizeInPersons):
        raise TypeError('max_size_of_studio_or_publisher must be a Studio_and_Publisher_Size')
    
    if max_size_of_studio != Studio.SizeInPersons.ARTISAN :
        # No filter on publisher size for non-artisan
        all_for_size = Videogame_common.objects.filter(studios__size_of_studio = max_size_of_studio).order_by("known_popularity").distinct()
    else :
        all_for_size = Videogame_common.objects.filter(studios__size_of_studio = Studio.SizeInPersons.ARTISAN, publishers__size_of_publisher = Publisher.SizeInPersons.ARTISAN).order_by("known_popularity").distinct()
    
    return all_for_size

def get_all_games_that_made_it() :
    # Here we don't care about the Publisher size
    all_for_size = Videogame_common.objects.filter(Q(studios__size_of_studio =  Studio.SizeInPersons.ARTISAN) | Q(studios__size_of_studio =  Studio.SizeInPersons.INDIE), ~Q(they_have_made_it = Videogame_common.TheyHaveMadeIt.NO))
    
    return all_for_size

def get_a_random_unfiltered_artisan_game(request) :
    found_game = get_a_random_game_for_size(Studio.SizeInPersons.ARTISAN)
    if found_game is None :
        return render(request, "thefiltershop/artisans_games.html", {"error_message": "No unfiltered artisans game found."})
    return game(request, found_game.id)

def get_a_random_unfiltered_indie_game(request) :
    found_game = get_a_random_game_for_size(Studio.SizeInPersons.INDIE)
    if found_game is None :
        return render(request, "thefiltershop/indies_games.html", {"error_message": "No unfiltered indie game found."})
    return game(request, found_game.id)

def get_a_random_game_for_size(max_size_of_studio) :
    ''' Find the max ID, get a limited number of entries (after filtering) at a random position from there '''
    if not isinstance(max_size_of_studio, Studio.SizeInPersons):
        raise TypeError('max_size_of_studio_or_publisher must be a Studio_and_Publisher_Size')
    
    if max_size_of_studio != Studio.SizeInPersons.ARTISAN :
        unfiltered_games = Videogame_common.objects.annotate(number_of_filters=Count('valueforfilter', filter=Q(valueforfilter__filter__is_positive=False))).filter( studios__size_of_studio = max_size_of_studio, number_of_filters = 0)
    else :
        unfiltered_games = Videogame_common.objects.annotate(number_of_filters=Count('valueforfilter', filter=Q(valueforfilter__filter__is_positive=False))).filter(studios__size_of_studio = Studio.SizeInPersons.ARTISAN, publishers__size_of_publisher = Publisher.SizeInPersons.ARTISAN, number_of_filters = 0)
        
    if len(unfiltered_games) >= 1 :
        max_games = unfiltered_games.count()
        
        print(str(unfiltered_games.query))
        
        random_pos = random.randint(0,max_games-1)
        
        print(f'Fetching at {random_pos} on {max_games}')
        
        game_to_show = unfiltered_games[random_pos]
    else :
        return None
            
    return game_to_show