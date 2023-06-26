from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from ..models import Videogame_common
from ..models import Studio
from ..models import Publisher
 
def index(request):
    # For small studio first
    #smallest_studio = Studio.objects.order_by("-known_popularity").order_by("-spotlight_count")[:5]
    
    # also with no publisher or a small one
    # Find the game with lowest time in the spotlight, and the fewer (bad) filters. Give a bonus for good filters
    latest_games = Videogame_common.objects.filter(Videogame_common.studios_set__size <= 5).filter(Videogame_common.publishers_set__size <= 5).order_by("-known_popularity").order_by("-spotlight_count")[:5]
    for aGame in latest_games:
        aGame.spotlight_count+=1
        aGame.save()
    
    context = {"latest_games": latest_games}
    return render(request, "thefiltershop/index.html", context)