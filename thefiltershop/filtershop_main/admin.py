from django.contrib import admin

# Register your models here.

from . import models

from django_object_actions import DjangoObjectActions, action

from django.http import HttpResponseRedirect
from django.urls import reverse

import requests
import logging

logger = logging.getLogger(__name__)

class FillModelFromJSONView(admin.AdminSite):
    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        my_urls = [
            path('thefiltershop/admin/fill_model_from_json/', self.fill_model_from_json, name='fill_model_from_json'),
        ]
        return my_urls + urls

    def fill_model_from_json(self, request):
        if request.method == 'POST':
            id = request.POST.get('id')
            if id:
                # Fetch JSON data from the API endpoint
                api_endpoint = f"http://www.apipoint.org/{id}"
                response = requests.get(api_endpoint)

                if response.status_code == 200:
                    # Load the JSON data
                    data = response.json()

                    # Update Game description from ID
                    for item in data:
                        video_game = models.Videogame_common(name=item['name'], description=item['short_description'], url=item['age'])
                        video_game.save()

                    self.message_user(request, "Person objects created successfully.")
                else:
                    self.message_user(request, "Failed to fetch JSON data from the API.")
            else:
                self.message_user(request, "Please provide an ID.")

            return HttpResponseRedirect(reverse('admin:yourapp_person_changelist'))

        context = {
            'opts': models.Videogame_common._meta,
            'app_label': models.Videogame_common._meta.app_label,
        }
        return self.render(request, 'admin/fill_model_from_json.html', context)
    
    # Text to put at the end of each page's <title>.
    site_title = 'The Filter Shop Admin page'

    # Text to put in each page's <h1> (and above login form).
    site_header = 'The Filter Shop Admin page'

    # Text to put at the top of the admin index page.
    index_title = 'The Filter Shop Admin main page'
        

admin_site = FillModelFromJSONView(name='customadmin')

admin.site.register(models.Profile)

class GeneralAdmin(admin.ModelAdmin):
    date_hierarchy = "date_creation"
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.create_user = request.user #create_user should only be set once
        obj.write_user = request.user #write_user can be set at all times
        super().save_model(request, obj, form, change)
        
@admin.register(models.Filter, models.TypeOfEntity, models.Entity_Category, models.ValueForFilter, models.Platform, models.Publisher, models.Online_Shop, models.Sponsor,
                models.Studio, models.Studio_type, models.Tag, site=admin_site)
class GeneralAdmin(admin.ModelAdmin):
    date_hierarchy = "date_creation"
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.create_user = request.user #create_user should only be set once
        obj.write_user = request.user #write_user can be set at all times
        super().save_model(request, obj, form, change)
   
class AliasInline(admin.StackedInline):
    model = models.Alias
    extra = 1
    
class ImagesInline(admin.StackedInline):
    model = models.Image
    extra = 3
    
#@admin.register(models.Image, site=admin_site)     
#class imageAdmin(admin.ModelAdmin):
#    list_display = ["title", "image_tag", "photo"] # new

class Links_to_shops_Inline(admin.StackedInline):
    model = models.Links_to_shops
    extra = 1
    
class Videogame_ratingInline(admin.StackedInline):
    model = models.Videogame_rating
    extra = 1
    
class EntityAdmin(admin.ModelAdmin):
    fieldsets = [
            ("General info", {"fields": ["name","description"]}),
            (None, {'fields': ['url','for_type','general_rating','vignette','hidden_full_cost','crapometer','in_hall_of_shame','descriptionOfShame', 'tags']}),
    ]
    
    inlines = [ImagesInline]
    
@admin.register(models.Entry_on_Steam, site=admin_site)
class EntryOnSteam(DjangoObjectActions, admin.ModelAdmin):

    @action(
        label="Fetch all full Video Game information from Steam"
    )
    @admin.action(description="Fetch the full Video Game information from Steam")
    def update_one_from_steam(modeladmin, request, queryset):
        id = queryset.appid
        logger.info(f"Will try to fetch using id {id} for {queryset}");
        if id:
            # check if Steam ID
            # Fetch JSON data from the API endpoint
            api_endpoint = f"https://store.steampowered.com/api/appdetails?appids={id}"
            response = requests.get(api_endpoint)
            if response.status_code == 200:
                # Load the JSON data
                data = response.json()
                # Check if success is true
                subdata = data[f"{id}"]
                success = subdata['success']
                if not success:
                    modeladmin.message_user(request, "Failed to fetch data from Steam, check the ID.")
                    return
                
                content = subdata['data']
                
                # If there is no video game type yet, create it
                try: 
                    video_game_type = models.TypeOfEntity.objects.all().get(name="Video Game") 
                except models.TypeOfEntity.DoesNotExist: 
                    video_game_type = models.TypeOfEntity(name="Video Game", description="A Video Game of all kind.")
                    video_game_type.save()
                # Check if updating or creating
                try: 
                    video_game = models.Videogame_common.objects.all().get(name=content['name']) 
                    modeladmin.message_user(request, f"{video_game.name} is already in the filter shop. Please use force update if you really want to update it.")
                except models.Videogame_common.DoesNotExist:               
                    
                    # Create Video Game from JSON data
                    
                    # Missing: game type, studio, publisher, platforms, vignette, link to shop (should be obvious)
                    video_game = models.Videogame_common(name=content['name'], description=content['short_description'], url=f"https://store.steampowered.com/app/{id}", for_type=video_game_type)
                    video_game.save()
                    modeladmin.message_user(request, "Information fetched successfully.")
            else:
                modeladmin.message_user(request, "Failed to fetch data from Steam, check the ID.")
        else:
            modeladmin.message_user(request, "Please provide an ID.")
    
    @action(
        label="Fetch all full Video Game information from Steam and force the update"
    )
    @admin.action(description="Fetch the full Video Game information from Steam and update the game entry even if it already exists")
    def force_update_one_from_steam(modeladmin, request, queryset):
        id = queryset.appid
        logger.info(f"Will try to fetch using id {id} for {queryset}");
        if id:
            # check if Steam ID
            # Fetch JSON data from the API endpoint
            api_endpoint = f"https://store.steampowered.com/api/appdetails?appids={id}"
            response = requests.get(api_endpoint)
            if response.status_code == 200:
                # Load the JSON data
                data = response.json()
                # Check if success is true
                subdata = data[f"{id}"]
                success = subdata['success']
                if not success:
                    modeladmin.message_user(request, "Failed to fetch data from Steam, check the ID.")
                    return
                
                content = subdata['data']
                
                # If there is no video game type yet, create it
                try: 
                    video_game_type = models.TypeOfEntity.objects.all().get(name="Video Game") 
                except models.TypeOfEntity.DoesNotExist: 
                    video_game_type = models.TypeOfEntity(name="Video Game", description="A Video Game of all kind.")
                    video_game_type.save()
                # Check if updating or creating
                try: 
                    video_game = models.Videogame_common.objects.all().get(name=content['name']) 
                    modeladmin.message_user(request, f"{video_game.name} is already in the filter shop. Updating all information from Steam.")
                    video_game.name = content['name']
                    video_game.description = content['short_description']
                    video_game.url = f"https://store.steampowered.com/app/{id}"
                    video_game.for_type =video_game_type
                    video_game.save()
                    
                except models.Videogame_common.DoesNotExist:               
                    
                    # Create Video Game from JSON data
                    
                    # Missing: game type, studio, publisher, platforms, vignette, link to shop (should be obvious)
                    video_game = models.Videogame_common(name=content['name'], description=content['short_description'], url=f"https://store.steampowered.com/app/{id}", for_type=video_game_type)
                    video_game.save()
                    modeladmin.message_user(request, "Information fetched successfully.")
            else:
                modeladmin.message_user(request, "Failed to fetch data from Steam, check the ID.")
        else:
            modeladmin.message_user(request, "Please provide an ID.")
            
    @action(
        label="Fetch all full Video Game information from Steam for all games missing in the filter shop"
    )
    @admin.action(description="Fetch the full Video Game information from Steam for all game known here and missing in the filter shop")
    def update_several_from_steam(modeladmin, request, queryset):
        for one_entry in queryset:
            print(one_entry)
            id = one_entry.appid
            logger.info(f"Will try to fetch using id {id}  for {one_entry}");
            if id:
                # check if Steam ID
                # Fetch JSON data from the API endpoint
                api_endpoint = f"https://store.steampowered.com/api/appdetails?appids={id}"
                response = requests.get(api_endpoint)

                if response.status_code == 200:
                    # Load the JSON data
                    data = response.json()
                    # Check if success is true
                    subdata = data[f"{id}"]

                    success = subdata['success']
                    if not success:
                        modeladmin.message_user(request, "Failed to fetch data from Steam, check the ID.")
                        return
                    
                    content = subdata['data']
                    
                    # If there is no video game type yet, create it
                    try: 
                        video_game_type = models.TypeOfEntity.objects.all().get(name="Video Game") 
                    except models.TypeOfEntity.DoesNotExist: 
                        video_game_type = models.TypeOfEntity(name="Video Game", description="A Video Game of all kind.")
                        video_game_type.save()

                    # Check if updating or creating
                    try: 
                        video_game = models.Videogame_common.objects.all().get(name=content['name']) 
                        modeladmin.message_user(request, f"{video_game.name} is already in the filter shop. Please use force update if you really want to update it.")
                    except models.Videogame_common.DoesNotExist:               
                        
                        # Create Video Game from JSON data
                        
                        # Missing: game type, studio, publisher, platforms, vignette, link to shop (should be obvious)
                        video_game = models.Videogame_common(name=content['name'], description=content['short_description'], url=f"https://store.steampowered.com/app/{id}", for_type=video_game_type)
                        video_game.save()

                        modeladmin.message_user(request, "Information fetched successfully.")
                else:
                    modeladmin.message_user(request, "Failed to fetch data from Steam, check the ID.")
            else:
                modeladmin.message_user(request, "Please provide an ID.")
            
    change_actions = ('update_one_from_steam', 'force_update_one_from_steam')
    changelist_actions = ('update_several_from_steam', )
    actions = [update_several_from_steam]
   
@admin.register(models.Videogame_common, site=admin_site)
class VideoGameAdmin(EntityAdmin):
    change_form_template = 'admin/change_form_with_game_site_fill_button.html'
    fieldsets = [
        (None, {"fields": ["game_type"]}),
        ("Ratings", {"fields": ["gameplay_rating","known_popularity","they_have_made_it"], "classes": ["collapse"]}),
        ("Made and published by", {"fields": ["studios","publishers","platforms"], "classes": ["collapse"]}),
    ]
    fieldsets.insert(0, EntityAdmin.fieldsets[0])
    
    inlines = [Videogame_ratingInline, AliasInline, Links_to_shops_Inline]
    
    inlines.insert(0, EntityAdmin.inlines[0])
    
    def save_model(self, request, obj, form, change):
        # Override the save_model method to include additional logic
        # Fetch images from the external website here and perform any necessary operations
        # For simplicity, let's assume the fetched images are stored in a variable called 'images'
        context = {
            'opts': models.Videogame_common._meta,
            'app_label': models.Videogame_common._meta.app_label,
        }
        
        logger.info("Using our custom save_model");
        
        # Will check if there is a Steam/Itch.io/Google Play/Apple ID and fetch the images from there if possible
        if request.method == 'POST':
            id = request.POST.get('external_id')
            logger.info(f"Will try to fetch using id {id}");
            if id:
                # check if Steam ID
                # Fetch JSON data from the API endpoint
                api_endpoint = f"https://store.steampowered.com/api/appdetails?appids={id}"
                response = requests.get(api_endpoint)

                if response.status_code == 200:
                    # Load the JSON data
                    data = response.json()

                    # Create Person objects from JSON data
                    for item in data:
                        video_game = models.Videogame_common(name=item['name'], description=item['short_description'], url=f"https://store.steampowered.com/app/{id}")
                        video_game.save()

                    self.message_user(request, "Information fetched successfully.")
                else:
                    self.message_user(request, "Failed to fetch data from Steam, check the ID.")
            else:
                self.message_user(request, "Please provide an ID.")

            return self.render(request, 'admin/change_form_with_game_site_fill_button.html', context)

        # Save the object
        super().save_model(request, obj, form, change)

        
@admin.register(models.Company_group, site=admin_site)
class Company_groupAdmin(EntityAdmin):
    fieldsets = [
        ("Made Details published by", {"fields": ["company_logo"]}),
    ]
    fieldsets.insert(0, EntityAdmin.fieldsets[0])
    
    inlines = [AliasInline]

@admin.register(models.Physical_shop, site=admin_site)
class Physical_shopAdmin(EntityAdmin):
    fieldsets = [
        (None, {"fields": ["shop_type"]}),
        ("Ratings", {"fields": ["ethical_rating","clarity_rating","they_have_made_it"], "classes": ["collapse"]}),
        ("Details", {"fields": ["shop_logo","group"], "classes": ["collapse"]}),
    ]
    fieldsets.insert(0, EntityAdmin.fieldsets[0])
    
    inlines = [AliasInline]
    
@admin.register(models.Software, site=admin_site)
class SoftwareAdmin(EntityAdmin):
    fieldsets = [
        (None, {"fields": ["software_type"]}),
        ("Ratings", {"fields": ["ethical_rating","clarity_rating","heaviness", "do_the_minimum", "they_have_made_it"], "classes": ["collapse"]}),
        ("Made and published by", {"fields": ["studios","publishers","platforms"], "classes": ["collapse"]}),
    ]
    fieldsets.insert(0, EntityAdmin.fieldsets[0])
    
    inlines = [AliasInline]