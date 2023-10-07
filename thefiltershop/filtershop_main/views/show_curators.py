from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from ..models import Profile

def get_curators(request):
    all_curators = Profile.objects.filter(curating_fields__name__exact="Video Game") # Would be only for group curator!

    context = {"all_curators": all_curators}

    return render(request, "thefiltershop/curators.html", context)