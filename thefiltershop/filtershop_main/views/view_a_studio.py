from django.shortcuts import render
from django.shortcuts import get_object_or_404

from ..models import Videogame_common
from ..models import Filter
from ..models import Links_to_shops
from ..models import Videogame_rating
from ..models import Studio
 
def studio(request, studio_id):
    a_studio = get_object_or_404(Studio, pk=studio_id)
            
    return render(request, "thefiltershop/studio.html", {"a_studio": a_studio)
    