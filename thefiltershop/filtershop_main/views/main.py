from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.db.models import Q
from django.db.models import Max
from django.db.models import Count
from django.views.generic import ListView

from datetime import datetime, timedelta, timezone
from  logging import Logger

from ..models import Videogame_common
from ..models import Filter
from ..models import Publisher
from ..models import Studio
 
from filtershop_main.constants import SPOTLIGHT_LIMIT
from filtershop_main.constants import Studio_and_Publisher_Size
 
# To do: show featured game (low popularity, low spotlight)
# Also cut by categories
def index(request):
    #latest_games = Videogame_common.objects.order_by("-date_creation")[:5]
    
    # Artisan first
    game_in_spotlight_artisan = get_game_for_spotlight(Studio_and_Publisher_Size.ARTISAN)
    if game_in_spotlight_artisan != None : 
        artisan_of_the_week_title_image =  game_in_spotlight_artisan.image_set.first()
        artisan_of_the_week_title_screenshots = game_in_spotlight_artisan.image_set.all()[2:]
        
        
    # Indie (bigger so)
    game_in_spotlight_indie = get_game_for_spotlight(Studio_and_Publisher_Size.INDIE)
    if game_in_spotlight_indie != None : 
        indie_of_the_week_title_image = game_in_spotlight_indie.image_set.first()
        indie_of_the_week_title_screenshots = game_in_spotlight_indie.image_set.all()[2:]
   
    # TODO: Other kinds: Top Big(ger) Studio, They could be in a top (now or at a later point?)
    context = {"artisan_of_the_week": game_in_spotlight_artisan, "artisan_of_the_week_title_image": artisan_of_the_week_title_image, "artisan_of_the_week_title_screenshots": artisan_of_the_week_title_screenshots,
               "indie_of_the_week": game_in_spotlight_indie, "indie_of_the_week_title_image": indie_of_the_week_title_image, "indie_of_the_week_title_screenshots": indie_of_the_week_title_screenshots,}

    return render(request, "thefiltershop/index.html", context)

def get_game_for_spotlight(max_size_of_studio_or_publisher) :
    if not isinstance(max_size_of_studio_or_publisher, Studio_and_Publisher_Size):
        raise TypeError('max_size_of_studio_or_publisher must be a Studio_and_Publisher_Size')

    min_size = max_size_of_studio_or_publisher.min
    max_size = max_size_of_studio_or_publisher.max
    
    # See if we already have a game to show
    if max_size_of_studio_or_publisher != Studio_and_Publisher_Size.ARTISAN :
        # No filter on publisher size for non-artisan
        last_in_spotlight = Videogame_common.objects.filter(in_the_spotlight=True, studios__size_in_persons__lt = max_size, studios__size_in_persons__gte = min_size)
    else :
        last_in_spotlight = Videogame_common.objects.filter(in_the_spotlight=True, studios__size_in_persons__lt = max_size, publishers__size_in_persons__lt = max_size)
    print(last_in_spotlight.query)
    
    if len(last_in_spotlight) > 1 :
        # We did something wrong somewhere
        Logger.warning("Got more than one game in the spotlight for Artisan, that should not happen!")
    elif len(last_in_spotlight) == 1 :
        game_in_spotlight = last_in_spotlight.first()
        # Check if still in the spotlight
        if (game_in_spotlight.spotlight_count > SPOTLIGHT_LIMIT and game_in_spotlight.in_the_spotlight_since  is None) or (game_in_spotlight.spotlight_count > SPOTLIGHT_LIMIT and datetime.now(timezone.utc).__gt__(game_in_spotlight.in_the_spotlight_since + timedelta(days=7))) :
            game_in_spotlight.in_the_spotlight = False
            game_in_spotlight.save(update_fields=['in_the_spotlight'])
            # TODO: when all game have the maximum spotlight_count, it should be restored to 0 for all
        else:
            # TODO: this allows one client to destroy one visibility... (auto refresh) So will need an higher count +  a protection against too many requests from one IP
            game_in_spotlight.spotlight_count+=1
            game_in_spotlight.save(update_fields=['spotlight_count'])
    else :
        # None yet, so we filter again    
        # no negative filter!
        if max_size_of_studio_or_publisher != Studio_and_Publisher_Size.ARTISAN :
            new_game_for_the_spotlight = Videogame_common.objects.annotate(number_of_filters=Count('valueforfilter', filter=Q(valueforfilter__filter__is_positive=False))).filter(studios__size_in_persons__lt = max_size, studios__size_in_persons__gte = min_size, number_of_filters = 0)
        else :
            new_game_for_the_spotlight = Videogame_common.objects.annotate(number_of_filters=Count('valueforfilter', filter=Q(valueforfilter__filter__is_positive=False))).filter(studios__size_in_persons__lt = max_size, publishers__size_in_persons__lt = max_size, number_of_filters = 0)
            
        if len(new_game_for_the_spotlight) == 1 :
            latest_games = new_game_for_the_spotlight.order_by("known_popularity").order_by("spotlight_count")[:1]
            print(str(latest_games.query))
            game_in_spotlight=latest_games.first()
            game_in_spotlight.in_the_spotlight = True
            game_in_spotlight.in_the_spotlight_since = datetime.now(timezone.utc)
            game_in_spotlight.spotlight_count+=1
            game_in_spotlight.save(update_fields=['spotlight_count','in_the_spotlight','in_the_spotlight_since'])
        else :
            # No game available...
            game_in_spotlight = None
    return game_in_spotlight