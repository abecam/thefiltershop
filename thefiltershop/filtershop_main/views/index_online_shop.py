from django.shortcuts import render
from ..models import Online_Shop

def index_online_shops(request):
    latest_shops = Online_Shop.objects.order_by("-date_creation")[:5]
    context = {"latest_shops": latest_shops}
    return render(request, "thefiltershop/index_online_shops.html", context)