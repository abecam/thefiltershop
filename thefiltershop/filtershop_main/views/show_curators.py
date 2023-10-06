from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from ..models import Profile

def get_curators(request):
    all_curators = Profile.objects.filter() # Would be only for group curator!

    paginator = Paginator(all_curators, 25)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}

    return render(request, "thefiltershop/curators.html", context)