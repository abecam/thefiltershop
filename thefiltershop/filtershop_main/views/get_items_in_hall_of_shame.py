from django.shortcuts import render

from ..models import Sponsor
from ..models import Studio
from ..models import Publisher
from ..models import Videogame_common
from ..models import Physical_shop
from ..models import Online_Shop


def get_items_in_hall_of_shame(request):
    nobody = True # If we have nobody there
    
    sponsors = Sponsor.objects.filter(in_hall_of_shame = True)
    studios = Studio.objects.filter(in_hall_of_shame = True)
    publishers = Publisher.objects.filter(in_hall_of_shame = True)
    games = Videogame_common.objects.filter(in_hall_of_shame = True)
    physical_shops = Physical_shop.objects.filter(in_hall_of_shame = True)
    online_shops = Online_Shop.objects.filter(in_hall_of_shame = True)
     
    if sponsors.count() + studios.count() + publishers.count() + games.count() + physical_shops.count() + online_shops.count() > 0 :
        nobody = False
    context = {"sponsors": sponsors, "studios": studios, "publishers": publishers, "games": games, "physical_shops": physical_shops, "online_shops": online_shops, "nobody": nobody}
    
    return render(request, "thefiltershop/hall_of_shame.html", context)