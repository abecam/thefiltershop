from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.db.models import F
from django.db.models import Max
from datetime import datetime, timedelta, timezone
from  logging import Logger

from ..models import Videogame_common
from ..models import Publisher
from ..models import Studio
from ..models import Online_Shop
 
from filtershop_main.constants import SPOTLIGHT_LIMIT
 
# To do: show featured game (low popularity, low spotlight)
# Also cut by categories
def index(request):
    #latest_games = Videogame_common.objects.order_by("-date_creation")[:5]
    
    # Artisan first
    
    # See if we already have a game to show
    last_in_spotlight = Videogame_common.objects.filter(in_the_spotlight=True, studios__size_in_persons__lt = 5, publishers__size_in_persons__lt = 5)
    
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
        # Small studio and small publisher, and no negative filter!
        game_from_artisan = Videogame_common.objects.filter(studios__size_in_persons__lt = 5, publishers__size_in_persons__lt = 5)
        latest_games = game_from_artisan.order_by("known_popularity").order_by("spotlight_count")[:1]
        print(str(latest_games.query))
        game_in_spotlight=latest_games.first()
        game_in_spotlight.in_the_spotlight = True
        game_in_spotlight.in_the_spotlight_since = datetime.now(timezone.utc)
        game_in_spotlight.spotlight_count+=1
        game_in_spotlight.save(update_fields=['spotlight_count','in_the_spotlight','in_the_spotlight_since'])

    current_spotlight = Videogame_common.objects.filter(in_the_spotlight=False, studios__size_in_persons__lt = 5, publishers__size_in_persons__lt = 5)
    latest_games = current_spotlight.order_by("-known_popularity").order_by("-spotlight_count")[:1]       
    
    # TODO: One game for Artisan, one for indie... 
    context = {"artisan_of_the_week": game_in_spotlight}
    return render(request, "thefiltershop/index.html", context)

# To do: 
# 
def game(request, videogame_id):
    a_game = get_object_or_404(Videogame_common, pk=videogame_id)
    return render(request, "thefiltershop/game.html", {"a_game": a_game})

def index_online_shops(request):
    latest_shops = Online_Shop.objects.order_by("-date_creation")[:5]
    context = {"latest_shops": latest_shops}
    return render(request, "thefiltershop/index_online_shops.html", context)

def online_shop(request, shop_id):
    a_game = get_object_or_404(Online_Shop, pk=shop_id)
    return render(request, "thefiltershop/online_shop.html", {"a_shop": a_game})