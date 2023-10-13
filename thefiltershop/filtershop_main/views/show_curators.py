from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from ..models import Profile

def get_curators(request):
    # Best contributors:
    # number_of_contrib in auth_group Curator 
    all_curators = Profile.objects.filter(user__groups__name ='Curator').order_by("-number_of_contrib")
    
    context = {"all_curators": all_curators}

    return render(request, "thefiltershop/curators.html", context)