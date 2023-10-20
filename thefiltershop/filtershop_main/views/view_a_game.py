from django.shortcuts import render
from django.shortcuts import get_object_or_404

from ..models import Videogame_common
from ..models import Filter
from ..models import Links_to_shops
from ..models import Videogame_rating
 
def game(request, videogame_id):
    a_game = get_object_or_404(Videogame_common, pk=videogame_id)
    is_filter = False
    negative_filters = Filter.objects.filter(valueforfilter__for_entity__pk = a_game.pk, valueforfilter__filter__is_positive=False)
    positive_filters = Filter.objects.filter(valueforfilter__for_entity__pk = a_game.pk,  valueforfilter__filter__is_positive=True)
    links_to_shops = Links_to_shops.objects.select_related("shop").filter(for_Entity=a_game.pk)
    ratings = Videogame_rating.objects.select_related("for_platform").filter(Videogame_common=a_game.pk)
    
    if negative_filters.count() + positive_filters.count() > 0 :
            is_filter = True
            
    # Now add the filters to the ratings queryset
    ratings_with_filters = []
    
    for one_rating in ratings.all():
        is_filter_rating = False
        
        negative_filters_this_rating = Filter.objects.filter(filtersforavideogamerating__for_rating__pk = one_rating.pk, filtersforavideogamerating__filter__is_positive=False)
        positive_filters_this_rating = Filter.objects.filter(filtersforavideogamerating__for_rating__pk = one_rating.pk,  filtersforavideogamerating__filter__is_positive=True)
        
        if negative_filters_this_rating.count() + positive_filters_this_rating.count() > 0 :
            is_filter_rating = True # Mostly useless currently, but good for consistency
            is_filter = True # At least one filter to show, so we want the button to appear!
            
        ratings_with_filters.append({"rating" :one_rating, "negative_filters": negative_filters_this_rating, "positive_filters": positive_filters_this_rating, "is_filter": is_filter_rating})
    
    print(ratings_with_filters)
    
    # Check if we have a description for the hidden full cost, otherwise show the default
    if a_game.description_hidden_full_cost and len(a_game.description_hidden_full_cost) > 0 :
        desc_hidden_full_cost = a_game.description_hidden_full_cost
    else :
        # 0 (none) to 50 (full price again (if not f2p)) to 80 (a lot more) to 100 (infinite, i.e. cannot be won whatever you spend)
        if a_game.hidden_full_cost == 0 :
            desc_hidden_full_cost = "None"
        elif a_game.hidden_full_cost < 20 :
            desc_hidden_full_cost = "Slightly more than described"
        elif a_game.hidden_full_cost < 40 :
            desc_hidden_full_cost = "Significantly more than described"
        elif a_game.hidden_full_cost < 60 :
            desc_hidden_full_cost = "Much more than described"
        elif a_game.hidden_full_cost < 80 :
            desc_hidden_full_cost = "A lot more than described, please check before buying!"
        elif a_game.hidden_full_cost < 100 :
            desc_hidden_full_cost = "Extremely high!"
        else :
            desc_hidden_full_cost = "Infinite, you cannot finish the game whatever you spend!"
            
    return render(request, "thefiltershop/game.html", {"a_game": a_game, "title_image": a_game.image_set.first(), "screenshots": a_game.image_set.all()[2:],
                                                       "negative_filters": negative_filters, "positive_filters": positive_filters, "is_filter": is_filter, 
                                                       "links_to_shops": links_to_shops.all(), "ratings_with_filters": ratings_with_filters, "desc_hidden_full_cost": desc_hidden_full_cost})
    