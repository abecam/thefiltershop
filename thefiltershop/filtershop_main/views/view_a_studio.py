from django.shortcuts import render
from django.shortcuts import get_object_or_404

from ..models import Videogame_common
from ..models import Filter
from ..models import Studio
 
def studio(request, studio_id):
    a_studio = get_object_or_404(Studio, pk=studio_id)
            
    is_filter = False
    negative_filters = Filter.objects.filter(valueforfilter__for_entity__pk = a_studio.pk, valueforfilter__filter__is_positive=False)
    positive_filters = Filter.objects.filter(valueforfilter__for_entity__pk = a_studio.pk,  valueforfilter__filter__is_positive=True)

    if negative_filters.count() + positive_filters.count() > 0 :
            is_filter = True
            
    games = Videogame_common.objects.filter(studios=a_studio.pk)

    print(games.query)

    return render(request, "thefiltershop/studio.html", {"a_studio": a_studio, 
                                                       "negative_filters": negative_filters, "positive_filters": positive_filters, "is_filter": is_filter, 
                                                       "games": games.all()} )
    