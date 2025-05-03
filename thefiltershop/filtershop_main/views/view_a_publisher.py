from django.shortcuts import render
from django.shortcuts import get_object_or_404

from ..models import Videogame_common
from ..models import Filter
from ..models import Publisher
 
def publisher(request, publisher_id):
    a_publisher = get_object_or_404(Publisher, pk=publisher_id)
            
    is_filter = False
    negative_filters = Filter.objects.filter(valueforfilter__for_entity__pk = a_publisher.pk, valueforfilter__filter__is_positive=False)
    positive_filters = Filter.objects.filter(valueforfilter__for_entity__pk = a_publisher.pk,  valueforfilter__filter__is_positive=True)

    if negative_filters.count() + positive_filters.count() > 0 :
            is_filter = True
            
    games = Videogame_common.objects.filter(publishers=a_publisher.pk)

    return render(request, "thefiltershop/publisher.html", {"a_publisher": a_publisher, 
                                                       "negative_filters": negative_filters, "positive_filters": positive_filters, "is_filter": is_filter, 
                                                       "games": games.all()} )
    