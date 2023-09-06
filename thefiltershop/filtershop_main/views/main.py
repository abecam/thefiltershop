from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import Http404

from ..models import Videogame_common
 
# To do: show featured game (low popularity, low spotlight)
# Also cut by categories
def index(request):
    latest_games = Videogame_common.objects.order_by("-date_creation")[:5]
    context = {"latest_games": latest_games}
    return render(request, "thefiltershop/index.html", context)


# To do: 
# 
def game(request, videogame_id):
    a_game = get_object_or_404(Videogame_common, pk=videogame_id)
    return render(request, "thefiltershop/game.html", {"a_game": a_game})