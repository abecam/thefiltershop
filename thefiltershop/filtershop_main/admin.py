from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.Profile)

@admin.register(models.Filter, models.TypeOfShop, models.TypeOfEntity, models.Entity_Category, models.ValueForFilter, models.Platform, models.Publisher, models.Shop, models.Sponsor,
                models.Studio, models.Studio_type, models.Tag)
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
    
@admin.register(models.Image)     
class imageAdmin(admin.ModelAdmin):
    list_display = ["title", "image_tag", "photo"] # new

class Videogame_ratingInline(admin.StackedInline):
    model = models.Videogame_rating
    extra = 1
    
class EntityAdmin(admin.ModelAdmin):
    fieldsets = [
            ("General info", {"fields": ["name","description"]}),
            (None, {'fields': ['url','for_type','general_rating','vignette','hidden_full_cost','crapometer','in_hall_of_shame','descriptionOfShame', 'tags']}),
    ]
   
@admin.register(models.Videogame_common)
class VideoGameAdmin(EntityAdmin):
    fieldsets = [
        (None, {"fields": ["game_type"]}),
        ("Ratings", {"fields": ["gameplay_rating","known_popularity","they_have_made_it"], "classes": ["collapse"]}),
        ("Made and published by", {"fields": ["studios","publishers","platforms"], "classes": ["collapse"]}),
    ]
    fieldsets.insert(0, EntityAdmin.fieldsets[0])
    
    inlines = [Videogame_ratingInline, AliasInline]
     
@admin.register(models.Company_group)
class Company_groupAdmin(EntityAdmin):
    fieldsets = [
        ("Made Details published by", {"fields": ["company_logo"]}),
    ]
    fieldsets.insert(0, EntityAdmin.fieldsets[0])
    
    inlines = [AliasInline]

@admin.register(models.Physical_shop)
class Physical_shopAdmin(EntityAdmin):
    fieldsets = [
        (None, {"fields": ["shop_type"]}),
        ("Ratings", {"fields": ["ethical_rating","clarity_rating","they_have_made_it"], "classes": ["collapse"]}),
        ("Details", {"fields": ["shop_logo","group"], "classes": ["collapse"]}),
    ]
    fieldsets.insert(0, EntityAdmin.fieldsets[0])
    
    inlines = [AliasInline]
    
@admin.register(models.Software)
class SoftwareAdmin(EntityAdmin):
    fieldsets = [
        (None, {"fields": ["software_type"]}),
        ("Ratings", {"fields": ["ethical_rating","clarity_rating","heaviness", "do_the_minimum", "they_have_made_it"], "classes": ["collapse"]}),
        ("Made and published by", {"fields": ["studios","publishers","platforms"], "classes": ["collapse"]}),
    ]
    fieldsets.insert(0, EntityAdmin.fieldsets[0])
    
    inlines = [AliasInline]