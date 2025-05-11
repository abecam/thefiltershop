import random
from django.shortcuts import render
from django.db.models import Q
from django.db.models import Count
from django.core.paginator import Paginator

from ..models import Videogame_common, Game_Category, Studio, Publisher, Recommended_Games_By_Contributor, Profile

def select_a_recommender(request):
    a_contributor = get_a_random_contributor(request.GET.get("level_of_contribution"))

    all_recommended_games = get_all_games_for_size()

    categories_in_recommended = set

    for a_game in all_recommended_games.all:
        categories_in_recommended.update(a_game.categories.all)

    game_categories = sorted(categories_in_recommended)

    context = {"recommender": a_contributor, "page_obj": all_recommended_games,"categories": game_categories, "selected_category": ""}

    return render(request, "thefiltershop/recommended.html", context)

def get_recommended_games(request):
    game_categories = request.GET.get('categories')
    recommender = request.GET.get('from')
    category_id = request.GET.get('category_id')  # Get the selected category ID from the query parameters
    page_number = request.GET.get("page")

    # Get all artisan games
    list_of_games_artisan = get_all_games_for_size(Studio.SizeInPersons.ARTISAN, recommender)

    # Apply category filtering if a category is selected
    if category_id:
        list_of_games_artisan = list_of_games_artisan.filter(categories__id=category_id)

    paginator = Paginator(list_of_games_artisan, 8)  

    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "categories": game_categories, "selected_category": category_id}

    return render(request, "thefiltershop/recommended.html", context)

def get_a_random_contributor(kind_of_contributor) :
    ''' Find the max ID, get a limited number of entries (after filtering) at a random position from there '''
    
    ## TODO: check if there is a difference here of replace the elif by an or
    if kind_of_contributor == "SU" :
        contributors = Profile.objects.annotate(filter( contribution_level = Profile.ContributorLevel.SUPER_SUPPORTER))
    elif kind_of_contributor == "SSU" :
        contributors = Profile.objects.annotate(filter( contribution_level = Profile.ContributorLevel.SUPPORTER))
    else :
        raise Warning(f'No contributors in the {kind_of_contributor} category.')
                
    if len(contributors) >= 1 :
        max_contributors = contributors.count()
        
        print(str(contributors.query))
        
        random_pos = random.randint(0,max_contributors-1)
        
        print(f'Fetching at {random_pos} on {max_contributors}')
        
        contributor_to_show = contributors[random_pos]
    else :
        raise Warning(f'No contributors in the {kind_of_contributor} category.')
            
    return contributor_to_show

def get_all_games_for_size(recommender) :
    
    all_games = Recommended_Games_By_Contributor.game.order_by("known_popularity")

    return all_games