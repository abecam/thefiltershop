import requests
import logging
import tempfile

from django.contrib import admin

# Register your models here.

from . import models

from django_object_actions import DjangoObjectActions, action

from django.http import HttpResponseRedirect
from django.urls import reverse



from django.core import files

logger = logging.getLogger(__name__)

class MyAdminSite(admin.AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = 'The Filter Shop Admin page'

    # Text to put in each page's <h1> (and above login form).
    site_header = 'The Filter Shop Admin page'

    # Text to put at the top of the admin index page.
    index_title = 'The Filter Shop Admin main page'
        

admin_site = MyAdminSite(name='customadmin')

admin.site.register(models.Profile)

class GeneralAdmin(admin.ModelAdmin):
    date_hierarchy = "date_creation"
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.create_user = request.user #create_user should only be set once
        obj.write_user = request.user #write_user can be set at all times
        super().save_model(request, obj, form, change)
      
    search_fields = ["name"]
      
@admin.register(models.TypeOfEntity, models.TypeOfRelationBetweenFilter, models.Entity_Category, models.ValueForFilter, models.Platform, models.Publisher, models.Online_Shop, models.Sponsor,
                models.Studio, models.Studio_type, models.Tag, site=admin_site)
class GeneralAdmin(GeneralAdmin):
    pass    
    
   
class RelatedFromFiltersInline(admin.StackedInline):
    model = models.RelatedFilters
    extra = 1
    classes = ['collapse']
    fk_name = "from_filter"
    verbose_name  = "Relation from filter (or both ways)"

class RelatedToFiltersInline(admin.StackedInline):
    model = models.RelatedFilters
    extra = 1
    classes = ['collapse']
    fk_name = "to_filter"
    verbose_name  = "Relation to filter (or both ways)"
    
class AliasInline(admin.StackedInline):
    model = models.Alias
    extra = 1
    classes = ['collapse']
    verbose_name = "Alias"
    verbose_name_plural = "Aliases"
    
class ImagesInline(admin.StackedInline):
    model = models.Image
    extra = 1
    classes = ['collapse']
    
#@admin.register(models.Image, site=admin_site)     
#class imageAdmin(GeneralAdmin):
#    list_display = ["title", "image_tag", "photo"] # new

class Links_to_shops_Inline(admin.StackedInline):
    model = models.Links_to_shops
    extra = 1
    
class Videogame_ratingInline(admin.StackedInline):
    model = models.Videogame_rating
    extra = 1
    
class EntityAdmin(GeneralAdmin):
    fieldsets = [
            ("General info", {"fields": ["name","description"]}),
            (None, {'fields': ['url','for_type','general_rating','vignette','hidden_full_cost','crapometer','in_hall_of_shame','descriptionOfShame', 'tags']}),
    ]
    
    inlines = [ImagesInline]
    
@admin.register(models.Filter, site=admin_site)
class FilterAdmin(GeneralAdmin):
    inlines = [RelatedFromFiltersInline, RelatedToFiltersInline]
    
@admin.register(models.New_Entry_on_Steam, site=admin_site)
class NewEntryOnSteam(DjangoObjectActions, GeneralAdmin):
    pass

@admin.register(models.Entry_on_Steam, site=admin_site)
class EntryOnSteam(DjangoObjectActions, GeneralAdmin):

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
                
                # Check if updating or creating
                try: 
                    video_game = models.Videogame_common.objects.all().get(name=content['name']) 
                    modeladmin.message_user(request, f"{video_game.name} is already in the filter shop. Please use force update if you really want to update it.")
                except models.Videogame_common.DoesNotExist:               
                    EntryOnSteam.getDataFromSteam(modeladmin, request, content, id)
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
                

                try: 
                    video_game = models.Videogame_common.objects.all().get(name=content['name']) 
                                    # If there is no video game type yet, create it
                    try: 
                        video_game_type = models.TypeOfEntity.objects.all().get(name="Video Game") 
                    except models.TypeOfEntity.DoesNotExist: 
                        video_game_type = models.TypeOfEntity(name="Video Game", description="A Video Game of all kind.")
                        video_game_type.save()
                    # Check if updating or creating
                
                    modeladmin.message_user(request, f"{video_game.name} is already in the filter shop. Updating all information from Steam.")
                    
                    # Would be better to reuse the getDataFromSteam but currently it would block on the images...
                    video_game.name = content['name']
                    video_game.description = content['short_description']
                    video_game.url = f"https://store.steampowered.com/app/{id}"
                    video_game.for_type = video_game_type
                    video_game.save()
                    
                except models.Videogame_common.DoesNotExist:               
                    EntryOnSteam.getDataFromSteam(modeladmin, request, content, id)
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
                    
                            # Check if updating or creating
                try: 
                    video_game = models.Videogame_common.objects.all().get(name=content['name']) 
                    modeladmin.message_user(request, f"{video_game.name} is already in the filter shop. Please use force update if you really want to update it.")
                except models.Videogame_common.DoesNotExist:
                    EntryOnSteam.getDataFromSteam(modeladmin, request, content, id)
                    
                else:
                    modeladmin.message_user(request, "Failed to fetch data from Steam, check the ID.")
            else:
                modeladmin.message_user(request, "Please select an item first.")
                
    def getDataFromSteam(modeladmin, request, content, id):
        # If there is no video game type yet, create it
        try: 
            video_game_type = models.TypeOfEntity.objects.all().get(name="Video Game") 
        except models.TypeOfEntity.DoesNotExist: 
            video_game_type = models.TypeOfEntity(name="Video Game", description="A Video Game of all kind.")
            video_game_type.save()

        # Create Video Game from JSON data

        # First check if not >18 - required_age	"18"
        if content['required_age'] == "18":
            modeladmin.message_user(request, "Sorry, the filter shop does not support mature content (yet).")
            return
        # Missing: game type, studio, publisher, platforms, vignette, link to shop (should be obvious)
        video_game = models.Videogame_common(name=content['name'], description=content['short_description'], url=content['website'] , for_type=video_game_type)

        # creating images
        # header_image

        # capsule_image
        #
        EntryOnSteam.getCapsuleAndHeader(content['capsule_image'],content['header_image'],video_game)
        # screenshots
        # screenshots	
        #   0	
        #   id	0
        # path_thumbnail	"https://cdn.akamai.steamstatic.com/steam/apps/1378660/ss_509aa0dc74d06b8a3544d62f2fd5b0b235c2ab84.600x338.jpg?t=1687509345"
        # path_full	"https://cdn.akamai.steamstatic.com/steam/apps/1378660/ss_509aa0dc74d06b8a3544d62f2fd5b0b235c2ab84.1920x1080.jpg?t=1687509345"
        EntryOnSteam.getAllThumbnails(content['screenshots'],video_game)
        # studio(s) and publisher(s)
        EntryOnSteam.setStudioAndPublisher(content['developers'],content['publishers'],video_game)

        # 
        EntryOnSteam.setPlatforms(content['platforms'],video_game)

        # Categories
        if 'genres' in content :
            EntryOnSteam.setCategories(content['genres'],video_game)

        # And the link to Steam
        EntryOnSteam.addLinkToSteam(id,video_game)
        video_game.save()

        # link to shop: f"https://store.steampowered.com/app/{id}"
        modeladmin.message_user(request, "Information fetched successfully.")
                        
    def getCapsuleAndHeader(capsule_url, header_url, model):
            # Stream the image from the url
            response = requests.get(capsule_url, stream=True)

            # Was the request OK?
            if response.status_code == requests.codes.ok:
                # Get the filename from the url, used for saving later
                file_name = model.name+"_capsule.jpg"
    
                # Create a temporary file
                lf = tempfile.NamedTemporaryFile()

                # Read the streamed image in sections
                for block in response.iter_content(1024 * 8):
        
                    # If no more file then stop
                    if not block:
                        break

                    # Write image block to temporary file
                    lf.write(block)

                # Save the temporary image to the model#
                # This saves the model so be sure that it is valid
                model.vignette.save(file_name, files.File(lf)) 
                #model.save()   
                    
            # Stream the image from the url
            response = requests.get(header_url, stream=True)

            # Was the request OK?
            if response.status_code == requests.codes.ok:
                # Get the filename from the url, used for saving later
                file_name =model.name+"_header.jpg"
    
                # Create a temporary file
                lf = tempfile.NamedTemporaryFile()

                # Read the streamed image in sections
                for block in response.iter_content(1024 * 8):
        
                    # If no more file then stop
                    if not block:
                        break

                    # Write image block to temporary file
                    lf.write(block)
                    
                image = models.Image()
                image.title = file_name
                image.Entity = model

                # Save the temporary image to the model#
                # This saves the model so be sure that it is valid
                image.photo.save(file_name, files.File(lf))   
            
    def getAllThumbnails(thumbnails, model):
        #
        #  screenshots
        #  screenshots	
        #   0	
        #   id	0
        # path_thumbnail	"https://cdn.akamai.steamstatic.com/steam/apps/1378660/ss_509aa0dc74d06b8a3544d62f2fd5b0b235c2ab84.600x338.jpg?t=1687509345"
        # path_full	"https://cdn.akamai.steamstatic.com/steam/apps/1378660/ss_509aa0dc74d06b8a3544d62f2fd5b0b235c2ab84.1920x1080.jpg?t=1687509345"
        #

        for nb_thumbnail, one_entry in enumerate(thumbnails):
            image_url = one_entry['path_thumbnail']
            
            # Stream the image from the url
            response = requests.get(image_url, stream=True)

            # Was the request OK?
            if response.status_code != requests.codes.ok:
                # Nope, error handling, skip file etc etc etc
                continue
    
            # Get the filename from the url, used for saving later
            file_name =f"{model.name}_thumbnail_{nb_thumbnail}.jpg"
            
            # Create a temporary file
            lf = tempfile.NamedTemporaryFile()

            # Read the streamed image in sections
            for block in response.iter_content(1024 * 8):
        
                # If no more file then stop
                if not block:
                    break

                # Write image block to temporary file
                lf.write(block)

            image = models.Image()
            image.title = file_name
            image.Entity = model

            # Save the temporary image to the model#
            # This saves the model so be sure that it is valid
            image.photo.save(file_name, files.File(lf))   
        
    def setStudioAndPublisher(developers,publishers,video_game):
        for one_entry in developers:
            print(one_entry)
            # Find back the developer or create it
            try: 
                studio = models.Studio.objects.all().get(name=one_entry) 
            except models.Studio.DoesNotExist: 
                studio = models.Studio(name=one_entry, description="")
                # And need a studio type first
                try: 
                    studioType = models.Studio_type.objects.all().get(name="Artisan") 
                except models.Studio_type.DoesNotExist: 
                    studioType = models.Studio_type(name="Artisan", description="Very small indie developer generally without publisher.", size_in_persons=0)
                    studioType.save()
                studio.type = studioType
                studio.save()
                
            # And add it
            video_game.studios.add(studio) 
                
        for one_entry in publishers:
            print(f"Publisher: {one_entry}")
            
            # Find back the publisher or create it
            try: 
                publisher = models.Publisher.objects.all().get(name=one_entry) 
            except models.Publisher.DoesNotExist: 
                publisher = models.Publisher(name=one_entry, description="")
                publisher.save()
    
             # And add it
            video_game.publishers.add(publisher) 
            
    def setPlatforms(platforms, video_game):
        # currently only a boolean for Windows, Linux and Mac
        if platforms['windows']:
            # Find back the Windows platform or create it
            try: 
                platform = models.Platform.objects.all().get(name="Windows") 
            except models.Platform.DoesNotExist: 
                platform = models.Platform(name="Windows", description="Windows 7 and after.")
                platform.save()
                
            # And add it
            video_game.platforms.add(platform)
        if platforms['linux']:
            # Find back the Linux platform or create it
            try: 
                platform = models.Platform.objects.all().get(name="Linux") 
            except models.Platform.DoesNotExist: 
                platform = models.Platform(name="Linux", description="Linux.")
                platform.save()
                
            # And add it
            video_game.platforms.add(platform)
            
        if platforms['mac']:
            # Find back the Linux platform or create it
            try: 
                platform = models.Platform.objects.all().get(name="Mac") 
            except models.Platform.DoesNotExist: 
                platform = models.Platform(name="Mac", description="Mac.")
                platform.save()   
                
            # And add it
            video_game.platforms.add(platform)
          
    def setCategories(genres,video_game):
        for one_entry in genres:
            print(one_entry)
            one_genre = one_entry['description']
            # Find back the developer or create it
            try: 
                category = models.Game_Category.objects.all().get(name=one_genre) 
            except models.Game_Category.DoesNotExist: 
                category = models.Game_Category(name=one_genre, description="")
                category.save()
                
             # And add it
            video_game.categories.add(category)
          
    def addLinkToSteam(steam_id, video_game):
        url=f"https://store.steampowered.com/app/{steam_id}"
        
        # Fond back the Steam shop or create it
        try: 
            steam_shop = models.Online_Shop.objects.all().get(name="Steam") 
        except models.Online_Shop.DoesNotExist: 
            steam_shop = models.Online_Shop(name="Steam", description="Steam, the biggest online store for Video Games", shop_type="Online Video Games for PC", ethical_rating=100, clarity_rating=100, 
                        spotlight_count = 0, they_have_made_it=1)
            
             # If there is no video game online shop type yet, create it
            try: 
                video_game_online_shop_type = models.TypeOfEntity.objects.all().get(name="Online Video Games Online Shop") 
            except models.TypeOfEntity.DoesNotExist: 
                video_game_online_shop_type = models.TypeOfEntity(name="Online Video Games Online Shop", description="An Online Shop selling Video Games also fully Online (no physical products or seldom).")
                video_game_online_shop_type.save()
                
            steam_shop.for_type = video_game_online_shop_type
                    
            steam_shop.save()
        
        linkToSteam = models.Links_to_shops(link=url, identity="Steam", shop=steam_shop, for_Entity=video_game)
        linkToSteam.save()
        
    @action(
        label="Refresh the list of all Video Game entries from Steam - warning, takes several minutes"
    )
    @admin.action(description="Fetch all Video Game referenced in Steam to populate this list")
    def fetch_all_from_steam(modeladmin, request, queryset):
        logger.info("Fetching all games from Steam");
        steam_api_url = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
        response = requests.get(steam_api_url)
        data = response.json()
        logger.info("Fetching all games from Steam - downloaded");
        
        models.New_Entry_on_Steam.objects.all().delete()
        
        logger.info("Fetching all games from Steam - all models deleted");
        
        # Populate the model
        for app_data in data['applist']['apps']:
            app_id = app_data['appid']
            app_name = app_data['name']
            
            # Update or create the model entry
            if "Demo" not in app_name: 
                models.New_Entry_on_Steam.objects.create(
                    appid=app_id,
                    name=app_name
                )
        
        # Now check if we got something and how many we got
        nb_new_games = models.New_Entry_on_Steam.objects.count() - models.Entry_on_Steam.objects.count()
        update_actual_entries = False
        if nb_new_games > 0 :
            logger.info(f"Fetching all games from Steam - all models created, got {nb_new_games} new applications");
            modeladmin.message_user(request, f"Fetching all games from Steam - all models created, got {nb_new_games} new applications")
            update_actual_entries = True
        elif nb_new_games < 0 :
            logger.info(f"Fetching all games from Steam - got too few models ({models.New_Entry_on_Steam.objects.count} - {-nb_new_games} less than already there)");
            modeladmin.message_user(request, f"Fetching all games from Steam - got too few models ({models.New_Entry_on_Steam.objects.count} - {-nb_new_games} less than already there), not updating.")
            update_actual_entries = True
        else :
            logger.info(f"Fetching all games from Steam - all models created, got no new applications (by number)");
            modeladmin.message_user(request, f"Fetching all games from Steam - all models created, got no new applications (by number)")
            update_actual_entries = True
        
        if update_actual_entries:
            models.Entry_on_Steam.objects.all().delete()
            
            for one_entry in models.New_Entry_on_Steam.objects.all():
               models.Entry_on_Steam.objects.create(
                    appid=one_entry.appid,
                    name=one_entry.name
                )

        modeladmin.message_user(request, "Finished.")
                
    change_actions = ('update_one_from_steam', 'force_update_one_from_steam')
    #changelist_actions = ('update_several_from_steam',)
    changelist_actions = ('fetch_all_from_steam',)
    actions = [update_several_from_steam]
    list_display = ["name", "appid"]
    ordering = ["name"]
    readonly_fields = ["name", "appid"]
    search_fields = ["name", "appid"]
   
@admin.register(models.Videogame_common, site=admin_site)
class VideoGameAdmin(EntityAdmin):
    list_filter = ["game_type", "platforms"]

    fieldsets = [
        (None, {"fields": ["game_type"]}),
        ("Ratings", {"fields": ["gameplay_rating","known_popularity","they_have_made_it"], "classes": ["collapse"]}),
        ("Made and published by", {"fields": ["studios","publishers","platforms"], "classes": ["collapse"]}),
    ]
    autocomplete_fields = ["studios","platforms"]
    search_fields = ["name"]
    
    fieldsets.insert(0, EntityAdmin.fieldsets[1])
    fieldsets.insert(0, EntityAdmin.fieldsets[0])
    
    inlines = [Videogame_ratingInline, AliasInline, Links_to_shops_Inline]
    
    inlines.insert(0, EntityAdmin.inlines[0])

        
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