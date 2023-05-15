from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.Person)

@admin.register(models.Entity, models.Platform, models.Publisher, models.Shop, models.Sponsor, models.Studio, models.Studio_type, models.Videogame_common, models.Videogame_rating, models.Tag)
class AuthorAdmin(admin.ModelAdmin):
    date_hierarchy = "date_creation"
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.create_user = request.user #create_user should only be set once
        obj.write_user = request.user #write_user can be set at all times
        super().save_model(request, obj, form, change)