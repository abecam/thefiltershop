from django.shortcuts import render
from django.shortcuts import get_object_or_404

from ..models import Videogame_common
from ..models import Filter
from ..models import Links_to_shops
 
def game(request, videogame_id):
    a_game = get_object_or_404(Videogame_common, pk=videogame_id)
    negative_filters = Filter.objects.filter(valueforfilter__for_entity__pk = a_game.pk, valueforfilter__filter__is_positive=False)
    positive_filters = Filter.objects.filter(valueforfilter__for_entity__pk = a_game.pk,  valueforfilter__filter__is_positive=True)
    links_to_shops = Links_to_shops.objects.select_related("shop").filter(for_Entity=a_game.pk)
    return render(request, "thefiltershop/game.html", {"a_game": a_game, "title_image": a_game.image_set.first(), "screenshots": a_game.image_set.all()[2:],
                                                       "negative_filters": negative_filters, "positive_filters": positive_filters, "links_to_shops": links_to_shops.all()})
    