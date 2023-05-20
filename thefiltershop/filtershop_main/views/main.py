from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from ..models import Videogame_common
 
def index(request):
    latest_games = Videogame_common.objects.order_by("-date_creation")[:5]
    template = loader.get_template("thefiltershop/index.html")
    context = {
        "latest_games": latest_games,
    }
    return HttpResponse(template.render(context, request))