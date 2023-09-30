from django.shortcuts import render
from django.shortcuts import get_object_or_404

from ..models import Online_Shop

# TODO: pushed in a different file
def index_online_shops(request):
    latest_shops = Online_Shop.objects.order_by("-date_creation")[:5]
    context = {"latest_shops": latest_shops}
    return render(request, "thefiltershop/index_online_shops.html", context)

def online_shop(request, shop_id):
    a_game = get_object_or_404(Online_Shop, pk=shop_id)
    return render(request, "thefiltershop/online_shop.html", {"a_shop": a_game})