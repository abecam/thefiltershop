
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from ..models import Filter
from ..models import RelatedFilters
from ..models import Videogame_common
from ..models import Studio
from ..models import Publisher
from ..models import Online_Shop
from ..models import Physical_shop
from ..models import TypeOfEntity

def get_all_filters(request):
    list_of_positive_filters = Filter.objects.filter(is_positive=True).distinct
    list_of_negative_filters = Filter.objects.filter(is_positive=False).distinct

    context = {"positive_filters": list_of_positive_filters, "negative_filters": list_of_negative_filters }

    return render(request, "thefiltershop/all_filters.html", context)

# Type of entity should be created first programmatically, then never touched again!
# We could push the type of entity as paramaeter, but it will render to a static template anyway...
def get_all_filters_for_an_entity_type_videogame(request):
    list_of_filter_for_video_games = Videogame_common.objects.select_related("for_type").values("for_type")

    list_of_negative_filters = Filter.objects.filter(typeofentity__id__in=list_of_filter_for_video_games, is_positive=False)
    list_of_positive_filters = Filter.objects.filter(typeofentity__id__in=list_of_filter_for_video_games, is_positive=True)

    list_of_filter_for_studios = Studio.objects.select_related("for_type").values("for_type")

    list_of_negative_filters_studios = Filter.objects.filter(typeofentity__id__in=list_of_filter_for_studios, is_positive=False)
    list_of_positive_filters_studios = Filter.objects.filter(typeofentity__id__in=list_of_filter_for_studios, is_positive=True)

    list_of_filter_for_publishers = Publisher.objects.select_related("for_type").values("for_type")

    list_of_negative_filters_publishers = Filter.objects.filter(typeofentity__id__in=list_of_filter_for_publishers, is_positive=False)
    list_of_positive_filters_publishers = Filter.objects.filter(typeofentity__id__in=list_of_filter_for_publishers, is_positive=True)

    context = {"positive_filters": list_of_positive_filters, "negative_filters": list_of_negative_filters, "positive_filters_studios": list_of_positive_filters_studios, "negative_filters_studios": list_of_negative_filters_studios,
               "positive_filters_publishers": list_of_positive_filters_publishers, "negative_filters_publishers": list_of_negative_filters_publishers }

    return render(request, "thefiltershop/game_filters.html", context)

def get_all_filters_for_an_entity_type_online_shop(request):
    list_of_filter_for_online_shops = Online_Shop.objects.select_related("for_type").values("for_type")
    list_of_negative_filters = Filter.objects.filter(typeofentity__id__in=list_of_filter_for_online_shops, is_positive=False)
    list_of_positive_filters = Filter.objects.filter(typeofentity__id__in=list_of_filter_for_online_shops, is_positive=True)
    
    context = {"positive_filters": list_of_positive_filters, "negative_filters": list_of_negative_filters }

    return render(request, "thefiltershop/online_shop_filters.html", context)

def get_all_filters_for_an_entity_type_physical_shop(request):
    list_of_filter_for_online_shops = Physical_shop.objects.select_related("for_type").values("for_type")

    list_of_negative_filters = Filter.objects.filter(typeofentity__id__in=list_of_filter_for_online_shops, is_positive=False)
    list_of_positive_filters = Filter.objects.filter(typeofentity__id__in=list_of_filter_for_online_shops, is_positive=True)

    context = {"positive_filters": list_of_positive_filters, "negative_filters": list_of_negative_filters }

    return render(request, "thefiltershop/physical_shop_filters.html", context)

def get_one_filter_and_related_filters(request, filter_id):
    a_filter = get_object_or_404(Filter, pk=filter_id)
    siblings_filters_from = RelatedFilters.objects.filter(to_filter__pk = filter_id, with_type__both_way=True)
    siblings_filters_to = RelatedFilters.objects.filter(from_filter__pk = filter_id,  with_type__both_way=True)
    children_filters = RelatedFilters.objects.filter(from_filter__pk = filter_id, with_type__both_way=False)
    parents_filters = RelatedFilters.objects.filter(to_filter__pk = filter_id,  with_type__both_way=False)
    
    return render(request, "thefiltershop/one_filter.html", {"a_filter": a_filter, "siblings_filters_from": siblings_filters_from, "siblings_filters_to": siblings_filters_to,
                                                       "children_filters": children_filters, "parents_filters": parents_filters})


