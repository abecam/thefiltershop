import random
import logging

from django.shortcuts import render
from django.core.paginator import Paginator

from django.shortcuts import get_object_or_404

from ..models import Profile, Sponsor

logger = logging.getLogger(__name__)

def get_recommended_games(request):
    recommender_id = request.GET.get('from')
    category_id = request.GET.get('category_id')  # Get the selected category ID from the query parameters
    page_number = request.GET.get("page")

    if recommender_id:
        a_recommender = get_object_or_404(Profile, pk=recommender_id)
    else:
        a_recommender = get_a_random_contributor(request.GET.get("level_of_contribution"))

    # Get all artisan games
    all_recommended_games = get_all_games_for_size(a_recommender)

    print(all_recommended_games)
    categories_in_recommended = all_recommended_games.first().categories.all()

    for a_game in all_recommended_games.all():
        categories_in_recommended= categories_in_recommended | a_game.categories.all()
    
    categories_in_recommended = categories_in_recommended.distinct().order_by("name")

    print(categories_in_recommended.query)

    # Apply category filtering if a category is selected
    if category_id:
        all_recommended_games = all_recommended_games.filter(categories__id=category_id)

    paginator = Paginator(all_recommended_games, 8)  

    page_obj = paginator.get_page(page_number)

    context = {"recommender": a_recommender,"page_obj": page_obj, "categories": categories_in_recommended, "selected_category": category_id}

    return render(request, "thefiltershop/recommended.html", context)

def get_recommended_games_by_sponsor(request):
    recommender_id = request.GET.get('from')
    category_id = request.GET.get('category_id')  # Get the selected category ID from the query parameters
    page_number = request.GET.get("page")

    if recommender_id:
        a_recommender = get_object_or_404(Sponsor, pk=recommender_id)
    else:
        a_recommender = get_a_random_sponsor()

    # Get all artisan games
    all_recommended_games = get_all_games_for_size_sponsor(a_recommender)

    print(all_recommended_games)
    categories_in_recommended = all_recommended_games.first().categories.all()

    for a_game in all_recommended_games.all():
        categories_in_recommended= categories_in_recommended | a_game.categories.all()
    
    categories_in_recommended = categories_in_recommended.distinct().order_by("name")

    print(categories_in_recommended.query)

    # Apply category filtering if a category is selected
    if category_id:
        all_recommended_games = all_recommended_games.filter(categories__id=category_id)

    paginator = Paginator(all_recommended_games, 8)  

    page_obj = paginator.get_page(page_number)

    context = {"recommender": a_recommender,"page_obj": page_obj, "categories": categories_in_recommended, "selected_category": category_id}

    return render(request, "thefiltershop/recommended_sponsor.html", context)

def get_a_random_contributor(kind_of_contributor) :
    ''' Find the max ID, get a limited number of entries (after filtering) at a random position from there '''
    
    ## TODO: check if there is a difference here of replace the elif by an or
    if kind_of_contributor == "SU" :
        contributors = Profile.objects.filter( contribution_level = Profile.ContributorLevel.SUPER_SUPPORTER)
    elif kind_of_contributor == "SSU" :
        contributors = Profile.objects.filter( contribution_level = Profile.ContributorLevel.SUPPORTER)
    elif kind_of_contributor == "CUR" :
        contributors = Profile.objects.filter( contribution_level = Profile.ContributorLevel.CURATOR)
    else :
        raise Warning(f'The {kind_of_contributor} category cannot recommend.')
                
    if len(contributors) >= 1 :
        max_contributors = contributors.count()
        
        print(str(contributors.query))
        
        random_pos = random.randint(0,max_contributors-1)
        
        print(f'Fetching at {random_pos} on {max_contributors}')
        
        contributor_to_show = contributors[random_pos]
    else :
        contributors = Profile.objects.filter()[:1]

        contributor_to_show = contributors[0]

        logger.warning(f'No contributors in the {kind_of_contributor} category.')
            
    return contributor_to_show

def get_all_games_for_size(recommender) :
    
    all_games = recommender.recommended_games.all().order_by("known_popularity")
                                                                                                                                             
    return all_games

def get_a_random_sponsor() :
    ''' Find the max ID, get a limited number of entries (after filtering) at a random position from there '''
    
    sponsors = Sponsor.objects.all()
                
    if len(sponsors) >= 1 :
        max_sponsors = sponsors.count()
        
        print(str(sponsors.query))
        
        random_pos = random.randint(0,max_sponsors-1)
        
        print(f'Fetching at {random_pos} on {max_sponsors}')
        
        sponsor_to_show = sponsors[random_pos]
    else :
        sponsors = Profile.objects.filter()[:1]

        sponsor_to_show = sponsors[0]

        logger.warning(f'No sponsors available.')
            
    return sponsor_to_show

def get_all_games_for_size_sponsor(recommender) :
    
    all_games = recommender.recommended_games.all().order_by("known_popularity")
                                                                                                                                             
    return all_games