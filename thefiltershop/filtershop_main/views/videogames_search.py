import random
import re

from django.shortcuts import render
from django.db.models import Q
from django.db.models import Count
from django.core.paginator import Paginator

from .view_a_game import game

from ..models import Videogame_common, Studio, Publisher, Filter

"""Search view for the video game category

    Description:
    Search through all categories related to video games and show them also in categories.
    Order should be: artisan games, indie games, other games, studios, publishers, filters
"""
    
def get_search_results(request):
    
    # Get the keywords from the string
    # TODO: support AND/OR and others
    keywords_txt = request.GET.get('keywords')
    
    # Split using space or comma
    keywords_not_curated = re.split(r';|,|\s', keywords_txt)
    # Remove if too short
    
    keywords = []
    
    for one_keyword in keywords_not_curated:
        one_keyword = one_keyword.strip()
        if len(one_keyword) >= 3 :
            keywords.append(one_keyword)
            print(f"One keyword {one_keyword}") 
        else :
            was_one_short_keyword = True
        
    if len(keywords) == 0 :
        if was_one_short_keyword :
            error = "Keyword must have at least 3 characters"
        else :
            error = "No keyword given"
        context = {"keywords" : request.GET.get('keywords'), "error": error}
    
        return render(request, "thefiltershop/search_page.html", context)
    
    
    # do start_with filter for our different elements, fill a dictionnary with the results
    found_artisan_games = get_all_games_for_keywords(keywords, Studio.SizeInPersons.ARTISAN)
    
    found_indie_games = get_all_games_for_keywords(keywords, Studio.SizeInPersons.INDIE)
    
    found_other_games = get_all_games_for_keywords(keywords, Studio.SizeInPersons.MEDIUM) | get_all_games_for_keywords(keywords, Studio.SizeInPersons.BIG) | get_all_games_for_keywords(keywords, Studio.SizeInPersons.HUGE)
    
    found_studios = get_all_studios_for_keywords(keywords)
    
    found_publishers = get_all_publishers_for_keywords(keywords)
    
    found_filters = get_all_filters_for_keywords(keywords)
    
    # render with all results
    # The paginator cannot be used as we have several querysets. It might need to be addressed if the returned sets are too long.
    context = {"artisan_games": found_artisan_games, "indie_games": found_indie_games, "other_games": found_other_games, "studios": found_studios, "publishers": found_publishers, "filters": found_filters}

    return render(request, "thefiltershop/vg_search_results.html", context)



def get_all_games_for_keywords(keywords, max_size_of_studio) :
    if not isinstance(max_size_of_studio, Studio.SizeInPersons):
        raise TypeError('max_size_of_studio_or_publisher must be a Studio_and_Publisher_Size')
    
    # Build-up the query string for keywords
    q_keyword = Q(name__icontains = keywords[0])

    if len(keywords) > 1 :
        for one_keyword in keywords[1:] :
            q_keyword = q_keyword | Q(name__icontains = one_keyword)
    
    if max_size_of_studio != Studio.SizeInPersons.ARTISAN :
        # No filter on publisher size for non-artisan
        all_for_size = Videogame_common.objects.filter(studios__size_of_studio = max_size_of_studio).filter(q_keyword).order_by("known_popularity").distinct()
    else :
        all_for_size = Videogame_common.objects.filter(studios__size_of_studio = Studio.SizeInPersons.ARTISAN, publishers__size_of_publisher = Publisher.SizeInPersons.ARTISAN).filter(q_keyword).order_by("known_popularity").distinct()
    print(all_for_size.query)
    return all_for_size

def get_all_studios_for_keywords(keywords) :
    # Build-up the query string for keywords
    q_keyword = Q(name__icontains = keywords[0])
    
    if len(keywords) > 1 :
        for one_keyword in keywords[1:] :
            q_keyword = q_keyword | Q(name__icontains = one_keyword)
    
    all_for_keyword = Studio.objects.filter(q_keyword)
     
    return all_for_keyword

def get_all_publishers_for_keywords(keywords) :
    # Build-up the query string for keywords
    q_keyword = Q(name__icontains = keywords[0])
    
    if len(keywords) > 1 :
        for one_keyword in keywords[1:] :
            q_keyword = q_keyword | Q(name__icontains = one_keyword)
    
    all_for_keyword = Publisher.objects.filter(q_keyword)
     
    return all_for_keyword

def get_all_filters_for_keywords(keywords) :
    # Build-up the query string for keywords
    q_keyword = Q(name__icontains = keywords[0])
    
    if len(keywords) > 1 :
        for one_keyword in keywords[1:] :
            q_keyword = q_keyword | Q(name__icontains = one_keyword)
    
    all_for_keyword = Filter.objects.filter(q_keyword)
     
    return all_for_keyword
