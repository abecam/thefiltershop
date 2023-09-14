from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.db.models import F
from django.db.models import Max

from ..models import Videogame_common
from ..models import Publisher
from ..models import Studio
from ..models import Online_Shop
 
# To do: show featured game (low popularity, low spotlight)
# Also cut by categories
def index(request):
    #latest_games = Videogame_common.objects.order_by("-date_creation")[:5]
    
    print(Videogame_common.objects)
    queryset = Videogame_common.objects.filter(studios__size_in_persons__lt = 5, publishers__size_in_persons__lt = 5)
    print(str(queryset.query))

    latest_games = queryset.order_by("-known_popularity").order_by("-spotlight_count")[:5]
    
    for aGame in latest_games:
        aGame.spotlight_count+=1
        aGame.save(update_fields=['spotlight_count'])
        
    context = {"latest_games": latest_games}
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