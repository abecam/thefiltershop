from django.shortcuts import render

from ..models import Sponsor

def get_sponsors(request):
    sponsors = Sponsor.objects.filter() # Would be only for group curator!

    context = {"sponsors": sponsors}

    return render(request, "thefiltershop/our_sponsors.html", context)