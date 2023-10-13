from django.shortcuts import render
from django.db.models import Q
from django.db.models import Count
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
    game_categories = Game_Category.objects.all()
    category_id = request.GET.get('category_id')  # Get the selected category ID from the query parameters
    
    list_of_games_indies = get_all_games_for_size(Studio.SizeInPersons.INDIE)

    # Apply category filtering if a category is selected
    if category_id:
        list_of_games_indies = list_of_games_indies.filter(categories__id=category_id)
        
    paginator = Paginator(list_of_games_indies, 8)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "categories": game_categories, "selected_category": category_id}

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

    context = {"page_obj": page_obj, "categories": game_categories, "selected_category": category_id}
    
    return render(request, "thefiltershop/they_made_it.html", context)

def get_best_of_the_rest(request):
    game_categories = Game_Category.objects.all()
    category_id = request.GET.get('category_id')  # Get the selected category ID from the query parameters
    
    # get_all_best_of_the_rest return a list, so the filtering for category needs to be done before.
    list_of_best_of_the_rest = get_all_best_of_the_rest(category_id)
        
    paginator = Paginator(list_of_best_of_the_rest, 25)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "categories": game_categories, "selected_category": category_id}

    return render(request, "thefiltershop/best_of_the_rest.html", context)

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
    all_for_size = Videogame_common.objects.filter(Q(studios__size_of_studio =  Studio.SizeInPersons.ARTISAN) | Q(studios__size_of_studio =  Studio.SizeInPersons.INDIE), ~Q(they_have_made_it = Videogame_common.TheyHaveMadeIt.NO))
    
    return all_for_size

def get_all_best_of_the_rest(for_category) :
    # On all filtered games, find which one would actually be good.
    # Best of the rest: gameplay_rating > 80 & good_wo_iap > 80 & good_wo_ads > 80 & use_psycho_tech == 0
    # ! -1 for good_wo_iap or good_wo_ads or use_psycho_tech means that they don't use it at all!
    if for_category is not None :
        # Apply category filtering if a category is selected
        pre_filterd_games = Videogame_common.objects.filter (categories__id=for_category)
        all_filtered_games = pre_filterd_games.annotate(number_of_filters=Count('valueforfilter', filter=Q(valueforfilter__filter__is_positive=False))).exclude( number_of_filters = 0).order_by("crapometer")[:100]
    else :
        all_filtered_games = Videogame_common.objects.annotate(number_of_filters=Count('valueforfilter', filter=Q(valueforfilter__filter__is_positive=False))).exclude( number_of_filters = 0).order_by("crapometer")[:100]
        
    # And exclude all that don't respect the rules
    remaining_games = []
    nb_of_remaing_games = 0
    
    for a_game in all_filtered_games :
        all_rating = a_game.videogame_rating_set.all()
        will_add = True
        for a_rating in all_rating :
            if a_rating.gameplay_rating < 80 or a_rating.good_wo_iap < 80 or a_rating.good_wo_ads < 80 or a_rating.use_psycho_tech > 0 :
                will_add = False
                print(f"Will exclude {a_game.name}")
                break
           
        if will_add :     
            remaining_games.append(a_game)      
            
        nb_of_remaing_games+=1
        
        if nb_of_remaing_games > 40 :
            break
        
    return remaining_games