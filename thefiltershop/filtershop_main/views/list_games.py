from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from ..models import Videogame_common
from filtershop_main.constants import Studio_and_Publisher_Size

def get_artisans_games(request):
    list_of_games_artisan = get_all_games_for_size(Studio_and_Publisher_Size.ARTISAN)

    paginator = Paginator(list_of_games_artisan, 25)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}

    return render(request, "thefiltershop/artisans_games.html", context)

def get_indies_games(request):
    list_of_games_indies = get_all_games_for_size(Studio_and_Publisher_Size.INDIE)

    paginator = Paginator(list_of_games_indies, 25)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}

    return render(request, "thefiltershop/indies_games.html", context)

def get_artisans_and_indies_games_that_made_it(request):
    list_of_games_that_made_it = get_all_games_that_made_it()

    paginator = Paginator(list_of_games_that_made_it, 25)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    
    return render(request, "thefiltershop/they_made_it.html", context)

def get_all_games_for_size(max_size_of_studio_or_publisher) :
    if not isinstance(max_size_of_studio_or_publisher, Studio_and_Publisher_Size):
        raise TypeError('max_size_of_studio_or_publisher must be a Studio_and_Publisher_Size')

    min_size = max_size_of_studio_or_publisher.min
    max_size = max_size_of_studio_or_publisher.max
    
    if max_size_of_studio_or_publisher != Studio_and_Publisher_Size.ARTISAN :
        # No filter on publisher size for non-artisan
        all_for_size = Videogame_common.objects.filter(studios__size_in_persons__lt = max_size, studios__size_in_persons__gte = min_size)
    else :
        all_for_size = Videogame_common.objects.filter(studios__size_in_persons__lt = max_size, publishers__size_in_persons__lt = max_size)
    
    return all_for_size

def get_all_games_that_made_it() :
    min_size = Studio_and_Publisher_Size.ARTISAN.min
    max_size = Studio_and_Publisher_Size.INDIE.max
    
    # Here we don't care about the Publisher size
    all_for_size = Videogame_common.objects.filter(studios__size_in_persons__lt = max_size, studios__size_in_persons__gte = min_size, they_have_made_it__gt = 0)
    
    return all_for_size