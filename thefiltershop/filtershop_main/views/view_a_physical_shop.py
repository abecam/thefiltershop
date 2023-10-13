from django.shortcuts import render
from django.shortcuts import get_object_or_404

from ..models import Physical_shop
from ..models import Filter
 
def physical_shop(request, shop_id):
    a_shop = get_object_or_404(Physical_shop, pk=shop_id)
    
    is_filter = False
    
    negative_filters = Filter.objects.filter(valueforfilter__for_entity__pk = shop_id, valueforfilter__filter__is_positive=False)
    positive_filters = Filter.objects.filter(valueforfilter__for_entity__pk = shop_id,  valueforfilter__filter__is_positive=True)
    
    if negative_filters.count() + positive_filters.count() > 0 :
            is_filter = True
            
    return render(request, "thefiltershop/physical_shop.html", {"a_shop": a_shop,
                                                       "negative_filters": negative_filters, "positive_filters": positive_filters, "is_filter": is_filter})
    