from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404

from ..models import Videogame_common
from ..models import Filter
 
def game(request, videogame_id):
    a_game = get_object_or_404(Videogame_common, pk=videogame_id)
    negative_filters = Filter.objects.filter(valueforfilter__for_entity__pk = a_game.pk, valueforfilter__filter__is_positive=False)
    positive_filters = Filter.objects.filter(valueforfilter__for_entity__pk = a_game.pk,  valueforfilter__filter__is_positive=True)
    
    return render(request, "thefiltershop/game.html", {"a_game": a_game, "title_image": a_game.image_set.first(), "screenshots": a_game.image_set.all()[2:],
                                                       "negative_filters": negative_filters, "positive_filters": positive_filters})
    