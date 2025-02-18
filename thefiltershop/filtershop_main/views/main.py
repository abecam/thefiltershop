from django.shortcuts import render
from django.db.models import Q
from django.db.models import Count

from datetime import datetime, timedelta, timezone
import logging

from ..models import Videogame_common, Studio, Publisher
 
from filtershop_main.constants import SPOTLIGHT_LIMIT

logger = logging.getLogger(__name__)
# To do: show featured game (low popularity, low spotlight)
# Also cut by categories
def index(request):
    #latest_games = Videogame_common.objects.order_by("-date_creation")[:5]
    
    # Artisan first
    game_in_spotlight_artisan = get_game_for_spotlight(Studio.SizeInPersons.ARTISAN)
    if game_in_spotlight_artisan != None : 
        artisan_of_the_week_title_image =  game_in_spotlight_artisan.image_set.first()
        artisan_of_the_week_title_screenshots = game_in_spotlight_artisan.image_set.all()[2:]
    else :
        artisan_of_the_week_title_image =  None
        artisan_of_the_week_title_screenshots = None
        
        
    # Indie (bigger so)
    game_in_spotlight_indie = get_game_for_spotlight(Studio.SizeInPersons.INDIE)
    if game_in_spotlight_indie != None : 
        indie_of_the_week_title_image = game_in_spotlight_indie.image_set.first()
        indie_of_the_week_title_screenshots = game_in_spotlight_indie.image_set.all()[2:]
    else :
        indie_of_the_week_title_image =  None
        indie_of_the_week_title_screenshots = None
   
    # TODO: Other kinds: Top Big(ger) Studio, They could be in a top (now or at a later point?)
    context = {"artisan_of_the_week": game_in_spotlight_artisan, "artisan_of_the_week_title_image": artisan_of_the_week_title_image, "artisan_of_the_week_title_screenshots": artisan_of_the_week_title_screenshots,
               "indie_of_the_week": game_in_spotlight_indie, "indie_of_the_week_title_image": indie_of_the_week_title_image, "indie_of_the_week_title_screenshots": indie_of_the_week_title_screenshots,}

    return render(request, "thefiltershop/index.html", context)

def get_game_for_spotlight(max_size_of_studio) :
    if not isinstance(max_size_of_studio, Studio.SizeInPersons):
        raise TypeError('max_size_of_studio_or_publisher must be a Studio_and_Publisher_Size')

    # See if we already have a game to show
    if max_size_of_studio != Studio.SizeInPersons.ARTISAN :
        # No filter on publisher size for non-artisan
        last_in_spotlight = Videogame_common.objects.filter(in_the_spotlight=True, studios__size_of_studio = max_size_of_studio).distinct()
    else :
        last_in_spotlight = Videogame_common.objects.filter(in_the_spotlight=True, studios__size_of_studio = Studio.SizeInPersons.ARTISAN, publishers__size_of_publisher = Publisher.SizeInPersons.ARTISAN).distinct()

    if len(last_in_spotlight) > 1 :
        # We did something wrong somewhere
        logger.warning("Got more than one game in the spotlight for Artisan, that should not happen!")
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
        if max_size_of_studio != Studio.SizeInPersons.ARTISAN :
            new_game_for_the_spotlight = Videogame_common.objects.annotate(number_of_filters=Count('valueforfilter', filter=Q(valueforfilter__filter__is_positive=False))).filter( studios__size_of_studio = max_size_of_studio, number_of_filters = 0).distinct()
        else :
            new_game_for_the_spotlight = Videogame_common.objects.annotate(number_of_filters=Count('valueforfilter', filter=Q(valueforfilter__filter__is_positive=False))).filter(studios__size_of_studio = Studio.SizeInPersons.ARTISAN, publishers__size_of_publisher = Publisher.SizeInPersons.ARTISAN, number_of_filters = 0).distinct()
        
        if len(new_game_for_the_spotlight) >= 1 :
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