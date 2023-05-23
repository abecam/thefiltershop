from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.safestring import mark_safe
from django.core.validators import MaxValueValidator, MinValueValidator

import PIL.Image

class User(AbstractUser):
    pass
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=300)
    biography = models.TextField(max_length=3000)
    
    nb_of_articles = models.IntegerField(editable=False, default=0)
    
    avatar = models.ImageField(
        default='avatar.jpg', # default avatar
        upload_to='profile_avatars' # dir to store the image
    )
    
    date_creation = models.DateTimeField("date creation", auto_now_add=True)
    last_update = models.DateTimeField("last updated", auto_now=True)
    
    def __str__(self):
        return f'{self.full_name} Profile'
    
    def save(self, *args, **kwargs):
        # save the profile first
        super().save(*args, **kwargs)

        # resize the image
        img = PIL.Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            # create a thumbnail
            img.thumbnail(output_size)
            # overwrite the larger image
            img.save(self.avatar.path)

class Filter(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(max_length=4000, null=True, blank=True)
    is_positive = models.BooleanField(default=False) # Fiters are mostly for bad things (too many IAPS, false Ads,... ) but could be positive too (educative, relaxing, ...)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, 
                                    verbose_name=('Created by'), editable=False, null=True, blank=True)
    date_creation = models.DateTimeField("date creation", auto_now_add=True)
    last_update = models.DateTimeField("last updated", auto_now=True)

class TypeOfShop(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(max_length=4000, null=True, blank=True)
    filters = models.ManyToManyField(Filter)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, 
                                    verbose_name=('Created by'), editable=False, null=True, blank=True)
    date_creation = models.DateTimeField("date creation", auto_now_add=True)
    last_update = models.DateTimeField("last updated", auto_now=True)
    
class TypeOfEntity(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(max_length=4000, null=True, blank=True)
    filters = models.ManyToManyField(Filter)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, 
                                    verbose_name=('Created by'), editable=False, null=True, blank=True)
    date_creation = models.DateTimeField("date creation", auto_now_add=True)
    last_update = models.DateTimeField("last updated", auto_now=True)
    
class Tag(models.Model):
    name = models.CharField(max_length=300)
    good_or_bad = models.IntegerField()
    parent_tag = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, 
                                    verbose_name=('Created by'), editable=False, null=True, blank=True)
    date_creation = models.DateTimeField("date creation", auto_now_add=True)
    last_update = models.DateTimeField("last updated", auto_now=True)
    
    def __str__(self):
        return self.name
    

########################################
class Shop(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(max_length=4000, null=True, blank=True)
    url = models.URLField()
    identity = models.ImageField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL,
                                    verbose_name=('Created by'), editable=False, null=True, blank=True)
    date_creation = models.DateTimeField("date creation", auto_now_add=True)
    last_update = models.DateTimeField("last updated", auto_now=True)
    
    def __str__(self):
        return self.name

########################################
class Links_to_shops(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(max_length=1000, null=True, blank=True)
    link = models.URLField()
    identity = models.CharField(max_length=300)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL,
                                    verbose_name=('Created by'), editable=False, null=True, blank=True)
    date_creation = models.DateTimeField("date creation", auto_now_add=True)
    last_update = models.DateTimeField("last updated", auto_now=True)
    
    def __str__(self):
        return self.name

class Entity_Category(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(max_length=3000, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL,
                                    verbose_name=('Created by'), editable=False, null=True, blank=True)
    date_creation = models.DateTimeField("date creation", auto_now_add=True)
    last_update = models.DateTimeField("last updated", auto_now=True)
    
class Entity(models.Model):
    # Ideally I would like an unique string id like type_product.publisher_name.studio_name.game_name
    # But I also don't think it should be a database ID (at least until the model is 100% set)
    name = models.CharField(max_length=300)
    url = models.URLField()
    for_type = models.ForeignKey(TypeOfEntity, on_delete=models.PROTECT)
    general_rating = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    
    vignette = models.ImageField(upload_to='images', null=False, blank=False)
    
    hidden_full_cost = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    crapometer = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    description = models.TextField(max_length=4000, null=True, blank=True)
    in_hall_of_shame = models.BooleanField()
    
    Links_to_shops = models.ForeignKey(Links_to_shops, on_delete=models.RESTRICT, null=True, blank=True)
    Entity_Category = models.ForeignKey(Entity_Category, on_delete=models.RESTRICT, null=True, blank=True)
    
    tags = models.ManyToManyField(Tag)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL,
                                    verbose_name=('Created by'), editable=False, null=True, blank=True)
    date_creation = models.DateTimeField("date creation", auto_now_add=True)
    last_update = models.DateTimeField("last updated", auto_now=True)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # save the profile first
        super().save(*args, **kwargs)

        # resize the image
        img = PIL.Image.open(self.vignette.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            # create a thumbnail
            img.thumbnail(output_size)
            # overwrite the larger image
            img.save(self.vignette.path)
            
    # ethical_money_rating = models.IntegerField()
    # ethical_moral_rating = models.IntegerField()
    # ethical_marketing_rating = models.IntegerField()
    # ethical_educational_rating = models.IntegerField()
    # cheating_review = models.IntegerField()
    # cheating_ads = models.IntegerField()
    # insulting_ads = models.IntegerField()
    # misleading_ads = models.IntegerField()
    # desc_cheating_ads = models.CharField(max_length=1000)
    # desc_insulting_ads = models.CharField(max_length=1000)
    # desc_misleading_ads = models.CharField(max_length=1000)
    
# ValueForFilter should be set-up by the application from the TypeOfEntity
class ValueForFilter(models.Model):
    value = models.IntegerField(null=False, default=50) # From 0 to 100
    filter = models.ForeignKey(Filter, on_delete=models.CASCADE, null=False)
    for_entity = models.ForeignKey(Entity, on_delete=models.CASCADE, null=False)
    description = models.TextField(max_length=1000, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL,
                                    verbose_name=('Created by'), editable=False, null=True, blank=True)
    date_creation = models.DateTimeField("date creation", auto_now_add=True)
    last_update = models.DateTimeField("last updated", auto_now=True)

class Image(models.Model):
    title = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='images')
    Entity = models.ForeignKey(Entity, null=True, blank=True, on_delete=models.CASCADE)

    def image_tag(self):
        return mark_safe('<img src="/../../media/%s" width="150" height="150" />' % (self.photo))

########################################
class Studio_type(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(max_length=1000, null=True, blank=True)
    size = models.IntegerField() # Size of the studio (0-> artisan, 10-> really big (>100))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL,
                                    verbose_name=('Created by'), editable=False, null=True, blank=True)
    date_creation = models.DateTimeField("date creation", auto_now_add=True)
    last_update = models.DateTimeField("last updated", auto_now=True)
    
    def __str__(self):
        return self.name
    
########################################
class Studio(models.Model):
    name_of_studio = models.CharField(max_length=300)
    type_of_studio = models.ForeignKey(Studio_type, on_delete=models.CASCADE)
    url = models.URLField()
    they_have_made_it = models.IntegerField(default=0, validators=[MaxValueValidator(3), MinValueValidator(0)]) # 'They have made it! (1-> Yes, 2->Yes partly thanks to us, 3->Yes mostly thanks to us) 
    money_rating = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)]) 
    fully_rotten = models.BooleanField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    in_hall_of_shame = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL,
                                    verbose_name=('Created by'), editable=False, null=True, blank=True)
    date_creation = models.DateTimeField("date creation", auto_now_add=True)
    last_update = models.DateTimeField("last updated", auto_now=True)
    
    def __str__(self):
        return self.name_of_studio

########################################
class Publisher(models.Model):
    name = models.CharField(max_length=300)
    size = models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)]) # Size of the publisher (0-> artisan, 10-> really big (>100))
    url = models.URLField()
    they_have_made_it = models.IntegerField(default=0, validators=[MaxValueValidator(3), MinValueValidator(0)]) # They have made it! (1-> Yes, 2->Yes partly thanks to us, 3->Yes mostly thanks to us)
    money_rating = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    fully_rotten = models.BooleanField(default=False)
    in_hall_of_shame = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL,
                                    verbose_name=('Created by'), editable=False, null=True, blank=True)
    date_creation = models.DateTimeField("date creation", auto_now_add=True)
    last_update = models.DateTimeField("last updated", auto_now=True)
    
    def __str__(self):
        return self.name

########################################
class Platform(models.Model):
    name = models.CharField(max_length=300)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL,
                                    verbose_name=('Created by'), editable=False, null=True, blank=True)
    date_creation = models.DateTimeField("date creation", auto_now_add=True)
    last_update = models.DateTimeField("last updated", auto_now=True)
    
    def __str__(self):
        return self.name
    
########################################
class Videogame_common(models.Model):
    game_type = models.CharField(max_length=300)
    gameplay_rating = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    known_popularity = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    spotlight_count = models.IntegerField(default=0)
    for_entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    they_have_made_it = models.IntegerField() # They have made it! (1-> Yes, 2->Yes partly thanks to us, 3->Yes mostly thanks to us)
    publishers =  models.ManyToManyField(Publisher)
    studios = models.ManyToManyField(Studio)
    platforms = models.ManyToManyField(Platform)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL,
                                    verbose_name=('Created by'), editable=False, null=True, blank=True)
    date_creation = models.DateTimeField("date creation", auto_now_add=True)
    last_update = models.DateTimeField("last updated", auto_now=True)
    
########################################
class Videogame_rating(models.Model):
    f2play = models.BooleanField(default=False)
    f2pay = models.BooleanField(default=False)
    gameplay_rating = models.IntegerField()
    money_rating = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    good_wo_iap = models.IntegerField(default=-1, validators=[MaxValueValidator(100), MinValueValidator(-1)])
    good_wo_ads = models.IntegerField(default=-1, validators=[MaxValueValidator(100), MinValueValidator(-1)])
    ads_supported = models.IntegerField(default=-1, validators=[MaxValueValidator(100), MinValueValidator(-1)])
    fully_rotten = models.BooleanField(default=False)
    would_be_good_if = models.TextField(max_length=1000)
    could_be_good_if = models.TextField(max_length=1000)
    use_psycho_tech = models.IntegerField(default=0)  
    Videogame_common = models.ForeignKey(Videogame_common, on_delete=models.CASCADE, null=True, blank=False)
    platform = models.ForeignKey(Platform, on_delete=models.PROTECT)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL,
                                    verbose_name=('Created by'), editable=False, null=True, blank=True)
    date_creation = models.DateTimeField("date creation", auto_now_add=True)
    last_update = models.DateTimeField("last updated", auto_now=True)
    
# Sponsor too (like a studio, type+size of contribution? +url)
########################################
class Sponsor(models.Model):
    name = models.CharField(max_length=300)
    url = models.URLField()
    description = models.TextField(max_length=1000)
    image = description = models.ImageField

    in_hall_of_shame = models.BooleanField()
    descriptionOfShame = models.TextField(max_length=1000)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL,
                                    verbose_name=('Created by'), editable=False, null=True, blank=True)
    date_creation = models.DateTimeField("date creation", auto_now_add=True)
    last_update = models.DateTimeField("last updated", auto_now=True)
    
    def __str__(self):
        return self.name_of_studio