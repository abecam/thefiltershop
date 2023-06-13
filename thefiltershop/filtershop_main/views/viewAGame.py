from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from ..models import Videogame_common
 
def index(request):
    latest_games = Videogame_common.objects.order_by("-date_creation")[:5]
    context = {"latest_games": latest_games}
    return render(request, "thefiltershop/index.html", context)