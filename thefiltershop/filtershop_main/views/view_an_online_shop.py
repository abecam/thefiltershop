from django.shortcuts import render
from django.shortcuts import get_object_or_404

from ..models import Online_Shop
from ..models import Filter
 
def online_shop(request, shop_id):
    a_shop = get_object_or_404(Online_Shop, pk=shop_id)
    negative_filters = Filter.objects.filter(valueforfilter__for_entity__pk = shop_id, valueforfilter__filter__is_positive=False)
    positive_filters = Filter.objects.filter(valueforfilter__for_entity__pk = shop_id,  valueforfilter__filter__is_positive=True)
    
    return render(request, "thefiltershop/online_shop.html", {"a_shop": a_shop,
                                                       "negative_filters": negative_filters, "positive_filters": positive_filters})
    