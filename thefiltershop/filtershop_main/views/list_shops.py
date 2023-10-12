from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator

from ..models import Online_Shop, Physical_shop, Game_Category, Studio, Publisher

def get_artisans_online_shops(request):
    type_of_shop = request.GET.get('shop_type')  # Get the selected category ID from the query parameters
    page_number = request.GET.get("page")

    # Get all artisan games
    list_of_shops_artisan = get_all_online_shop_for_artisans_or_others(Online_Shop.SizeInPersons.ARTISAN)
    all_found_types = get_all_types_of_online_shop()
    
    # Apply category filtering if a category is selected
    if type_of_shop:
        list_of_shops_artisan = list_of_shops_artisan.filter(shop_type=type_of_shop)

    paginator = Paginator(list_of_shops_artisan, 8)  

    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "types": all_found_types, "selected_type": type_of_shop}

    return render(request, "thefiltershop/online_artisans_shops.html", context)


def get_indies_online_shops(request):
    type_of_shop = request.GET.get('shop_type')  # Get the selected category ID from the query parameters
    page_number = request.GET.get("page")

    # Get all artisan games
    list_of_shops_artisan = get_all_online_shop_for_artisans_or_others(Online_Shop.SizeInPersons.INDIE)
    all_found_types = get_all_types_of_online_shop()
    
    # Apply category filtering if a category is selected
    if type_of_shop:
        list_of_shops_artisan = list_of_shops_artisan.filter(shop_type=type_of_shop)

    paginator = Paginator(list_of_shops_artisan, 8)  

    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "types": all_found_types, "selected_type": type_of_shop}

    return render(request, "thefiltershop/online_indies_shops.html", context)

def get_others_online_shops(request):
    type_of_shop = request.GET.get('shop_type')  # Get the selected category ID from the query parameters
    page_number = request.GET.get("page")
    
    list_of_shops = get_all_online_shop_for_artisans_or_others(None)
    all_found_types = get_all_types_of_online_shop()

   # Apply category filtering if a category is selected
    if type_of_shop:
        list_of_shops = list_of_shops.filter(shop_type=type_of_shop)
        
    paginator = Paginator(list_of_shops, 25)  # Show 25 contacts per page.
    
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "types": all_found_types, "selected_type": type_of_shop}

    return render(request, "thefiltershop/online_other_shops.html", context)

def get_artisans_and_indies_shops_that_made_it(request):
    list_of_games_that_made_it = get_all_online_shops_that_made_it()

    paginator = Paginator(list_of_games_that_made_it, 25)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    
    return render(request, "thefiltershop/they_made_it_online_shops.html", context)

def get_all_online_shop_for_artisans_or_others(max_size_of_shop) :
    if not max_size_of_shop :
        # All excepted ARTISAN and INDIE
        all_for_size = Online_Shop.objects.exclude(size_of_shop = Online_Shop.SizeInPersons.ARTISAN).exclude(size_of_shop = Publisher.SizeInPersons.INDIE)
    elif max_size_of_shop != Online_Shop.SizeInPersons.ARTISAN :
        # No filter on publisher size for non-artisan
        all_for_size = Online_Shop.objects.filter(size_of_shop = max_size_of_shop)
    else :
        all_for_size = Online_Shop.objects.filter(size_of_shop = Online_Shop.SizeInPersons.ARTISAN)
    
    return all_for_size

def get_all_online_shops_that_made_it():
    # Here we don't care about the Publisher size
    all_for_size = Online_Shop.objects.filter(Q(size_of_shop =  Online_Shop.SizeInPersons.ARTISAN) | Q(size_of_shop =  Online_Shop.SizeInPersons.INDIE), ~Q(they_have_made_it = Online_Shop.TheyHaveMadeIt.NO))
    
    return all_for_size

def get_all_types_of_online_shop():
    return Online_Shop.objects.all().values_list("shop_type").distinct()

### Physical shop
def get_artisans_physical_shops(request):
    type_of_shop = request.GET.get('shop_type')  # Get the selected category ID from the query parameters
    page_number = request.GET.get("page")

    # Get all artisan games
    list_of_shops_artisan = get_all_physical_shop_for_artisans_or_others(Physical_shop.SizeInPersons.ARTISAN)
    all_found_types = get_all_types_of_physical_shop()
    
    # Apply category filtering if a category is selected
    if type_of_shop:
        list_of_shops_artisan = list_of_shops_artisan.filter(shop_type=type_of_shop)

    paginator = Paginator(list_of_shops_artisan, 8)  

    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "types": all_found_types, "selected_type": type_of_shop}

    return render(request, "thefiltershop/physical_artisans_shops.html", context)


def get_indies_physical_shops(request):
    type_of_shop = request.GET.get('shop_type')  # Get the selected category ID from the query parameters
    page_number = request.GET.get("page")

    # Get all artisan games
    list_of_shops_artisan = get_all_physical_shop_for_artisans_or_others(Physical_shop.SizeInPersons.INDIE)
    all_found_types = get_all_types_of_physical_shop()
    
    # Apply category filtering if a category is selected
    if type_of_shop:
        list_of_shops_artisan = list_of_shops_artisan.filter(shop_type=type_of_shop)

    paginator = Paginator(list_of_shops_artisan, 8)  

    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "types": all_found_types, "selected_type": type_of_shop}

    return render(request, "thefiltershop/physical_indies_shops.html", context)

def get_others_physical_shops(request):
    type_of_shop = request.GET.get('shop_type')  # Get the selected category ID from the query parameters
    page_number = request.GET.get("page")
    
    list_of_shops = get_all_physical_shop_for_artisans_or_others(None)
    all_found_types = get_all_types_of_physical_shop()

   # Apply category filtering if a category is selected
    if type_of_shop:
        list_of_shops = list_of_shops.filter(shop_type=type_of_shop)
        
    paginator = Paginator(list_of_shops, 25)  # Show 25 contacts per page.
    
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "types": all_found_types, "selected_type": type_of_shop}

    return render(request, "thefiltershop/physical_other_shops.html", context)

def get_artisans_and_indies_physical_shops_that_made_it(request):
    list_of_games_that_made_it = get_all_physical_shops_that_made_it()

    paginator = Paginator(list_of_games_that_made_it, 25)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    
    return render(request, "thefiltershop/they_made_it_physical_shops.html", context)

def get_all_physical_shop_for_artisans_or_others(max_size_of_shop) :
    if not max_size_of_shop :
        # All excepted ARTISAN and INDIE
        all_for_size = Physical_shop.objects.exclude(size_of_shop = Physical_shop.SizeInPersons.ARTISAN).exclude(size_of_shop = Physical_shop.SizeInPersons.INDIE)
    elif max_size_of_shop != Physical_shop.SizeInPersons.ARTISAN :
        # No filter on publisher size for non-artisan
        all_for_size = Physical_shop.objects.filter(size_of_shop = max_size_of_shop)
    else :
        all_for_size = Physical_shop.objects.filter(size_of_shop = Physical_shop.SizeInPersons.ARTISAN)
    
    return all_for_size

def get_all_physical_shops_that_made_it():
    # Here we don't care about the Publisher size
    all_for_size = Physical_shop.objects.filter(Q(size_of_shop =  Physical_shop.SizeInPersons.ARTISAN) | Q(size_of_shop =  Physical_shop.SizeInPersons.INDIE), ~Q(they_have_made_it = Physical_shop.TheyHaveMadeIt.NO))
    
    return all_for_size

def get_all_types_of_physical_shop():
    return Physical_shop.objects.all().values_list("shop_type").distinct()