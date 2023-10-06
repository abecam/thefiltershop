from django.shortcuts import render
from django.shortcuts import get_object_or_404

from ..models import Physical_shop

def index_physical_shops(request):
    latest_shops = Physical_shop.objects.order_by("-date_creation")[:5]
    context = {"latest_shops": latest_shops}
    return render(request, "thefiltershop/index_physical_shops.html", context)
