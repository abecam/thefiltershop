import requests
import logging
import tempfile

from django.contrib import admin
from django.db.models import F
from django.core import files
from datetime import timedelta
from django.utils import timezone
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Register your models here.

from . import models

from django_object_actions import DjangoObjectActions, action



logger = logging.getLogger(__name__)

class MyAdminSite(admin.AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = 'The Filter Shop Admin page'

    # Text to put in each page's <h1> (and above login form).
    site_header = 'The Filter Shop Admin page'

    # Text to put at the top of the admin index page.
    index_title = 'The Filter Shop Admin main page'
        

admin_site = MyAdminSite(name='customadmin')

class Recommended_Games_By_Sponsor(admin.TabularInline):
    model = models.Recommended_Games_By_Sponsor
    autocomplete_fields = (
        'game',
    )
    xtra = 2
    verbose_name = "Recommended game"
    verbose_name_plural = "Recommended games"    
@admin.register(models.Profile, site=admin_site)
class ProfileAdmin(admin.ModelAdmin):
    exclude= ['number_of_contrib', 'last_changed_by']
    
@admin.register(models.User, models.Group, site=admin_site)
class USerGroupAdmin(admin.ModelAdmin):
    exclude= ['last_changed_by']

@admin.register(models.TypeOfEntity, models.TypeOfRelationBetweenFilter, models.Entity_Category, models.Platform, models.Tag, site=admin_site)
class GeneralAdmin(admin.ModelAdmin):
    date_hierarchy = "date_creation"
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        print("Saving various info!")
        if not obj.pk:
            obj.created_by = request.user #create_user should only be set once
        obj.last_changed_by.add(request.user)
        profile_for_user = models.Profile.objects.get(user__pk = request.user.id)
        profile_for_user.number_of_contrib = F("number_of_contrib") + 1
        profile_for_user.save()
        
        #super().save_model(request, obj, form, change)
      
    search_fields = ["name"]
    exclude= ['last_changed_by']

@admin.register(models.Review, site=admin_site) 
class Review(GeneralAdmin):
    exclude= ['description', 'last_changed_by']
    list_display = ["name", "profile", "game", "note"]

@admin.register(models.Sponsor, site=admin_site) 
class Sponsor(GeneralAdmin):
    inlines = [Recommended_Games_By_Sponsor]
    list_display = ["name", "in_hall_of_shame"]

@admin.register(models.Publisher,
                models.Studio, site=admin_site) 
class ElementWithHallOfShame(GeneralAdmin):
    list_display = ["name", "in_hall_of_shame"]
    
class FiltersForAVideoGameRating(admin.TabularInline) :
    model = models.FiltersForAVideoGameRating
    extra = 0
    verbose_name = "Filtered for this platform with"
    verbose_name_plural = "Applied filters for this platform"
    
class ValueForFilterAdmin(admin.TabularInline) :
    model = models.ValueForFilter
    extra = 0
    verbose_name = "Filtered with"
    verbose_name_plural = "Applied filters"

class RelatedFromFiltersInline(admin.TabularInline):
    model = models.RelatedFilters
    extra = 1
    classes = ['collapse']
    fk_name = "to_filter"
    verbose_name  = "Relation from filter (or both ways) - Like parents to this filter"

class RelatedToFiltersInline(admin.TabularInline):
    model = models.RelatedFilters
    extra = 1
    classes = ['collapse']
    fk_name = "from_filter"
    verbose_name  = "Relation to filter (or both ways) - Like children to this filter"
    
class AliasInline(admin.TabularInline):
    model = models.Alias
    extra = 1
    classes = ['collapse']
    verbose_name = "Alias"
    verbose_name_plural = "Aliases"
    
class ImagesInline(admin.TabularInline):
    model = models.Image
    extra = 1
    classes = ['collapse']
    
#@admin.register(models.Image, site=admin_site)     
#class imageAdmin(GeneralAdmin):
#    list_display = ["title", "image_tag", "photo"] # new

class Links_to_shops_Inline(admin.TabularInline):
    model = models.Links_to_shops
    extra = 0
    verbose_name = "On Sale on"
    verbose_name_plural = "On Sale on"
    
class Videogame_ratingInline(admin.StackedInline):
    model = models.Videogame_rating
    extra = 0
    verbose_name = "Rating for one platform"
    verbose_name_plural = "Ratings by platforms"
    
    exclude = ['name','last_changed_by']
        
@admin.register(models.Videogame_rating, site=admin_site)
class Videogame_rating(GeneralAdmin):

    inlines = [FiltersForAVideoGameRating]
    exclude = ['name','last_changed_by']
    
    # Calculate the crapometer value when saving
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        # form.instance stores the saved object
         # Calculate the crapometer value
        # Number of negative filters and their values
        game_negative_filters = models.FiltersForAVideoGameRating.objects.filter(for_rating__pk = form.instance.id, filter__is_positive=False)

        value_neg_filters = 0
        for a_filter in game_negative_filters :
            value_neg_filters+=a_filter.value

        if (value_neg_filters > 300) :
            value_neg_filters = 300
        form.instance.crapometer = (100*value_neg_filters)/300
        form.instance.save()
        
 
class EntityAdmin(GeneralAdmin):
    fieldsets = [
            ("General info", {"fields": ["name","description","headline"]}),
            (None, {'fields': ['url', 'for_type', 'general_rating', 'vignette', 'hidden_full_cost', 'description_hidden_full_cost', 'in_hall_of_shame', 'descriptionOfShame', 'tags']}),
    ]
    autocomplete_fields = ["tags"]
    
    inlines = [ValueForFilterAdmin, ImagesInline]
    
@admin.register(models.Filter, site=admin_site)
class FilterAdmin(GeneralAdmin):
    inlines = [RelatedFromFiltersInline, RelatedToFiltersInline]
    
@admin.register(models.New_Entry_on_Steam, site=admin_site)
class NewEntryOnSteam(admin.ModelAdmin):
    list_display = ["name", "appid"]
    ordering = ["name"]
    readonly_fields = ["name", "appid"]
    search_fields = ["name", "appid"]

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
                    modeladmin.message_user(request, f"Failed to fetch data from Steam, check the ID ({id}).")
                    return
                
                content = subdata['data']
                
                # Check if updating or creating
                try: 
                    video_game = models.Videogame_common.objects.all().get(name=content['name']) 
                    modeladmin.message_user(request, f"{video_game.name} is already in the filter shop. Please use force update if you really want to update it.")
                except models.Videogame_common.DoesNotExist:               
                    EntryOnSteam.getDataFromSteam(modeladmin, request, content, id)
                    
                    # Update the known popularity (nb of reviews in Steam)
                    EntryOnSteam.get_review_count(modeladmin, request, queryset)
            else:
                modeladmin.message_user(request, f"Failed to fetch data from Steam, check the ID ({id}).")
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
                    modeladmin.message_user(request, f"Failed to fetch data from Steam, check the ID ({id}).")
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
                    
                    # Update the known popularity (nb of reviews in Steam)
                    EntryOnSteam.get_review_count(modeladmin, request, queryset)
                    
                except models.Videogame_common.DoesNotExist:               
                    EntryOnSteam.getDataFromSteam(modeladmin, request, content, id)
            else:
                modeladmin.message_user(request, f"Failed to fetch data from Steam, check the ID ({id}).")
        else:
            modeladmin.message_user(request, "Please provide an ID.")
            
    @action(
        label="Fetch all full Video Game information from Steam for all games missing in the filter shop"
    )
    @admin.action(description="Fetch the full Video Game information from Steam for all game known here and missing in the filter shop")
    def update_several_from_steam(modeladmin, request, queryset):
        for one_entry in queryset:
            print('one entry to update ->',one_entry)
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
                        modeladmin.message_user(request, f"Failed to fetch data from Steam, check the ID ({id}).")
                        return
                    
                    content = subdata['data']
                    
                            # Check if updating or creating
                try: 
                    video_game = models.Videogame_common.objects.all().get(name=content['name']) 
                    modeladmin.message_user(request, f"{video_game.name} is already in the filter shop. Please use force update if you really want to update it.")
                except models.Videogame_common.DoesNotExist:
                    EntryOnSteam.getDataFromSteam(modeladmin, request, content, id)
                    
                    # Update the known popularity (nb of reviews in Steam)
                    EntryOnSteam.get_review_count(modeladmin, request, one_entry)
                else:
                    modeladmin.message_user(request, f"Failed to fetch data from Steam, check the ID ({id}).")
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

        if not "publishers" in content :
            publishers = content['developers']

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
                # We migh need to create the studio type first
                try: 
                    studio_type = models.TypeOfEntity.objects.all().get(name="Studio") 
                except models.TypeOfEntity.DoesNotExist: 
                    studio_type = models.TypeOfEntity(name="Studio", description="A Studio creating Video Games or Applications.")
                    studio_type.save()
                studio.for_type = studio_type

                ### Need a vignette too
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
                # We migh need to create the studio type first
                try: 
                    publisher_type = models.TypeOfEntity.objects.all().get(name="Publisher") 
                except models.TypeOfEntity.DoesNotExist: 
                    publisher_type = models.TypeOfEntity(name="Publisher", description="A Publisher publishing Video Games or Applications.")
                    publisher_type.save()
                publisher.for_type = publisher_type

                ### Need a vignette too
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
                        spotlight_count = 0, they_have_made_it=models.Online_Shop.TheyHaveMadeIt.YES)
            
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
            if  app_name and not app_name.endswith(" Demo") and not app_name.endswith(" Playtest") and not app_name.endswith(" Pack") and not app_name.endswith(" Soundtrack") and not app_name.endswith(" DLC") and not app_name.endswith(" Add-On") and not app_name.endswith(" Trailer") and not app_name.endswith(" OST") and not app_name.endswith(" Pack)") and not app_name.endswith(" Activation") and not app_name.endswith(" Artbook") and not app_name.endswith(" Server") and not app_name.endswith(" Season Pass") and not app_name.endswith(" Content") and not app_name.endswith(" Outfit") and not app_name.endswith(" Package") and not app_name.endswith(" Expansion") and not app_name.endswith(" Upgrade") and not app_name.endswith(" Editor") and "18+" not in app_name : 
                # Keep all the remaining extension so we can filter them out eventually
                all_names = app_name.split()
                if len(all_names) > 1 :
                    models.AllEndStringFromSteam.objects.create(name=all_names[-1]);
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
           
    @action(
        label="Fetch the known popularity from Steam. Also fetched during the original import!"
    )
    @admin.action(description="Fetch the known popularity from Steam")
    def update_popularity_from_steam(modeladmin, request, queryset):
        nbOfUpdate = 0
        
        for one_entry in queryset:
            if EntryOnSteam.get_review_count(modeladmin, request, one_entry) :
                nbOfUpdate+= 1
        
        modeladmin.message_user(request, f"Done! Updated {nbOfUpdate} games") 
   
    def get_review_count(modeladmin, request, one_entry):
        print('one entry to update ->',one_entry)
        app_id = one_entry.appid
        logger.info(f"Will try to fetch using id {app_id} for {one_entry}");
        if app_id:
            with urlopen(f"https://store.steampowered.com/app/{app_id}") as response:
                soup = BeautifulSoup(response, 'html.parser')
                if soup:
                    reviewCount = soup.find(itemprop="reviewCount")
                    if reviewCount :
                        reviewCountContent = int(reviewCount.get("content"))
               
                        print(reviewCountContent)
                
                        try:
                            video_game = models.Videogame_common.objects.all().get(name=one_entry.name) 
                            if reviewCountContent > 200 :
                                reviewCountContent = 200
                            if reviewCountContent < 11 :
                                reviewCountContent = 0
                            video_game.known_popularity = reviewCountContent / 2
                            video_game.save()
                            return True
                        except models.Videogame_common.DoesNotExist:
                            modeladmin.message_user(request, f"{one_entry.name} does not seem to exist in the filter shop yet.")
                    else:
                        modeladmin.message_user(request, f"No review yet for {one_entry.name}.")
                else:
                    modeladmin.message_user(request, f"Could not fetch the Steam page for {one_entry.name}.")
        else:
            modeladmin.message_user(request, "Please select an item first.")
            
        return False
                                    
    change_actions = ('update_one_from_steam', 'force_update_one_from_steam')
    #changelist_actions = ('update_several_from_steam',)
    changelist_actions = ('fetch_all_from_steam',)
    actions = [update_several_from_steam, update_popularity_from_steam]
    list_display = ["name", "appid"]
    ordering = ["name"]
    readonly_fields = ["name", "appid"]
    search_fields = ["name", "appid"]
   
   
# Category is also a part of Entity... But then it will be one filtering more to restrict to game.
@admin.register(models.Game_Category, site=admin_site)
class Videogame_CategoryAdmin(admin.ModelAdmin):
    model = models.Game_Category
    extra = 0
    search_fields = ["name"]
    exclude = ['last_changed_by']
    
@admin.register(models.Videogame_common, site=admin_site)
class VideoGameAdmin(DjangoObjectActions, EntityAdmin):
    list_filter = ["game_type", "platforms"]

    fieldsets = [
        (None, {"fields": ["game_type","categories","link_sold_from_dev","special_sale","special_bonuses","are_special_bonuses_global","general_sale"]}),
        ("Ratings", {"fields": ["gameplay_rating","known_popularity","they_have_made_it"], "classes": ["collapse"]}),
        ("Made and published by", {"fields": ["studios","publishers","platforms"]}),
    ]
    autocomplete_fields = ["studios","publishers","platforms","categories"]
    autocomplete_fields.insert(0, EntityAdmin.autocomplete_fields[0])
    
    search_fields = ["name"]
    
    fieldsets.insert(0, EntityAdmin.fieldsets[1])
    fieldsets.insert(0, EntityAdmin.fieldsets[0])
    
    inlines = [Videogame_ratingInline, Links_to_shops_Inline, AliasInline]
    
    inlines.insert(0, EntityAdmin.inlines[0])
    
    list_display = ["name", "they_have_made_it", "in_the_spotlight", "in_hall_of_shame"]
    
    @action(
        label="Check the spotlight count and reset it to 0 for all if needed."
    )
    @admin.action(description="Fetch all Video Game referenced in Steam to populate this list")
    def check_spotlight_count(modeladmin, request, queryset):
        logger.info("Getting all game that hasn't been in the spotlight for more than 1 year");
        
        time_threshold = timezone.now() - timedelta(days=365)
        last_in_spotlight = models.Videogame_common.objects.filter(in_the_spotlight=False, in_the_spotlight_since__lte=time_threshold)
        
        # Now check if we got something and how many we got
        if last_in_spotlight.count() == 0 :
            logger.info(f"No games to reset yet");
            modeladmin.message_user(request, "No games to reset yet.")
            return

        logger.info(f"Will reset {last_in_spotlight.count()} games");
        
        for aGame in last_in_spotlight:
            #aGame.spotlight_count = 0
            logger.info(f"Would have resetted {aGame.name}")
        modeladmin.message_user(request, f"Finished, for {last_in_spotlight.count()} games.")
                
    changelist_actions = ('check_spotlight_count',)
   
    # Calculate the crapometer value when saving
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        # form.instance stores the saved object
         # Calculate the crapometer value
        # Here strickly the number of negative filters and their values
        game_negative_filters = models.ValueForFilter.objects.filter(for_entity__pk = form.instance.id, filter__is_positive=False)

        value_neg_filters = 0
        for a_filter in game_negative_filters :
            value_neg_filters+=a_filter.value

        if (value_neg_filters > 300) :
            value_neg_filters = 300
        form.instance.crapometer = (100*value_neg_filters)/300
        form.instance.save()
        
        # Now populate the name for the related ratings
        game_ratings= models.Videogame_rating.objects.filter(Videogame_common__pk = form.instance.id)
        
        for a_game_rating in game_ratings:
            # Name is name of the game + name of the platform
            for_platform = a_game_rating.for_platform.name
            if a_game_rating.same_platform_alternative_shop:
                a_game_rating.name = f"{form.instance.name} for {for_platform} on {a_game_rating.same_platform_alternative_shop}"
            else:
                print(form.instance.name)
                print(for_platform)
                a_game_rating.name = f"{form.instance.name} for {for_platform}"
                print(a_game_rating.name)
                
            a_game_rating.save()

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
        (None, {"fields": ["shop_type", "size_of_shop"]}),
        ("Ratings", {"fields": ["ethical_rating","clarity_rating","they_have_made_it"], "classes": ["collapse"]}),
        ("Details", {"fields": ["group"], "classes": ["collapse"]}),
    ]
    
    fieldsets.insert(0, EntityAdmin.fieldsets[1])
    fieldsets.insert(0, EntityAdmin.fieldsets[0])
    
    inlines = [AliasInline]
    inlines.insert(0, EntityAdmin.inlines[0])
    
    list_display = ["name", "they_have_made_it", "in_the_spotlight", "in_hall_of_shame"]

    # Calculate the crapometer value when saving
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        # form.instance stores the saved object
         # Calculate the crapometer value
        # Number of negative filters and their values
        game_negative_filters = models.ValueForFilter.objects.filter(for_entity__pk = form.instance.id, filter__is_positive=False)

        value_neg_filters = 0
        for a_filter in game_negative_filters :
            value_neg_filters+=a_filter.value

        if (value_neg_filters > 300) :
            value_neg_filters = 300
        form.instance.crapometer = (100*value_neg_filters)/300
        form.instance.save()
        
@admin.register(models.Online_Shop, site=admin_site)
class Online_shopAdmin(EntityAdmin):
    fieldsets = [
        (None, {"fields": ["shop_type", "size_of_shop"]}),
        ("Ratings", {"fields": ["ethical_rating","clarity_rating","they_have_made_it"], "classes": ["collapse"]}),
        ("Details", {"fields": ["group"], "classes": ["collapse"]}),
    ]
    
    fieldsets.insert(0, EntityAdmin.fieldsets[1])
    fieldsets.insert(0, EntityAdmin.fieldsets[0])
    
    inlines = [AliasInline]
    inlines.insert(0, EntityAdmin.inlines[0])
    
    list_display = ["name", "they_have_made_it", "in_the_spotlight", "in_hall_of_shame"]
    
    # Calculate the crapometer value when saving
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        # form.instance stores the saved object
         # Calculate the crapometer value
        # Number of negative filters and their values
        game_negative_filters = models.ValueForFilter.objects.filter(for_entity__pk = form.instance.id, filter__is_positive=False)

        value_neg_filters = 0
        for a_filter in game_negative_filters :
            value_neg_filters+=a_filter.value

        if (value_neg_filters > 300) :
            value_neg_filters = 300
        form.instance.crapometer = (100*value_neg_filters)/300
        form.instance.save()
    
@admin.register(models.Software, site=admin_site)
class SoftwareAdmin(EntityAdmin):
    fieldsets = [
        (None, {"fields": ["software_type"]}),
        ("Ratings", {"fields": ["ethical_rating", "they_have_made_it"], "classes": ["collapse"]}),
        ("Made and published by", {"fields": ["studios","publishers","platforms"], "classes": ["collapse"]}),
    ]
    fieldsets.insert(0, EntityAdmin.fieldsets[0])
    
    inlines = [AliasInline]
    
    list_display = ["name", "they_have_made_it", "in_the_spotlight", "in_hall_of_shame"]
    
    # Calculate the crapometer value when saving
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        # form.instance stores the saved object
         # Calculate the crapometer value
        # Number of negative filters and their values
        game_negative_filters = models.ValueForFilter.objects.filter(for_entity__pk = form.instance.id, filter__is_positive=False)

        value_neg_filters = 0
        for a_filter in game_negative_filters :
            value_neg_filters+=a_filter.value

        if (value_neg_filters > 300) :
            value_neg_filters = 300
        form.instance.crapometer = (100*value_neg_filters)/300
        form.instance.save()