from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.utils.safestring import mark_safe
from django.core.validators import MaxValueValidator, MinValueValidator

import PIL.Image

class User(AbstractUser):
    pass

class Group(Group):
    pass
    
class BaseModel(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(max_length=1000, null=True, blank=True)
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, 
                                    verbose_name=('created by'), editable=False, null=True, blank=True, related_name="%(app_label)s_%(class)s_related_type")
    date_creation = models.DateTimeField("date creation", auto_now_add=True)
    last_update = models.DateTimeField("last updated", auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        abstract = True
        ordering = ['date_creation', 'name']
        
class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=300)
    biography = models.TextField(max_length=3000)
    
    nb_of_articles = models.IntegerField(editable=False, default=0)
    
    avatar = models.ImageField(
        default='avatar.jpg', # default avatar
        upload_to='profile_avatars' # dir to store the image
    )

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

class Filter(BaseModel):
    is_positive = models.BooleanField(default=False) # Fiters are mostly for bad things (too many IAPS, false Ads,... ) but could be positive too (educative, relaxing, ...)

    long_description = models.TextField(max_length=20000, null=True, blank=True)
    what_to_change = models.TextField(max_length=20000, null=True, blank=True)
    
class TypeOfRelationBetweenFilter(BaseModel):
    both_way = models.BooleanField(null=False, default=False) # False -> from to, True -> both way
    
# Relation to filter with a base model (i.e. name and description) so as to define the nature of the relation
class RelatedFilters(BaseModel):
    from_filter = models.ForeignKey(Filter, on_delete=models.CASCADE, null=False, related_name="from_filter")
    to_filter = models.ForeignKey(Filter, on_delete=models.CASCADE, null=False, related_name="to_filter")
    with_type = models.ForeignKey(TypeOfRelationBetweenFilter, on_delete=models.PROTECT)
    
class TypeOfEntity(BaseModel):
    filters = models.ManyToManyField(Filter)

    
class Tag(BaseModel):
    good_or_bad = models.IntegerField()
    parent_tag = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    
class Entity(BaseModel):
    # Ideally I would like an unique string id like type_product.publisher_name.studio_name.game_name
    # But I also don't think it should be a database ID (at least until the model is 100% set)
    headline = models.CharField(max_length=500, null=True, blank=True) # Line to show if on the front page
    url = models.URLField(null=True)
    for_type = models.ForeignKey(TypeOfEntity, on_delete=models.PROTECT, related_name="%(app_label)s_%(class)s_related_type")
    general_rating = models.IntegerField(default=50, validators=[MaxValueValidator(100), MinValueValidator(0)])
    
    vignette = models.ImageField(upload_to='images', null=True, blank=False)
    
    hidden_full_cost = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    crapometer = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    in_hall_of_shame = models.BooleanField(default=False)
    descriptionOfShame = models.TextField(max_length=1000, null=True, blank=True)
    
    tags = models.ManyToManyField(Tag, related_name="%(app_label)s_%(class)s_related_tags", blank=True)

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
    
# Should be inline in Entities. 
class Alias(BaseModel):
    for_entity = models.ForeignKey(Entity, on_delete=models.CASCADE, null=False)

class Entity_Category(BaseModel):
    for_Entity = models.ForeignKey(Entity, on_delete=models.RESTRICT, null=True, blank=True)
        
# ValueForFilter should be set-up by the application from the TypeOfEntity
class ValueForFilter(BaseModel):
    value = models.IntegerField(null=False, default=50, validators=[MaxValueValidator(100), MinValueValidator(0)]) # From 0 to 100
    filter = models.ForeignKey(Filter, on_delete=models.CASCADE, null=False)
    for_entity = models.ForeignKey(Entity, on_delete=models.CASCADE, null=False)

class Image(models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='images')
    Entity = models.ForeignKey(Entity, null=True, blank=True, on_delete=models.CASCADE)

    def image_tag(self):
        return mark_safe('<img src="/../../media/%s" width="150" height="150" />' % (self.photo))

class ImageForFilter(BaseModel):
    title = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='images')
    Filter = models.ForeignKey(Filter, null=True, blank=True, on_delete=models.CASCADE)

    def image_tag(self):
        return mark_safe('<img src="/../../media/%s" width="150" height="150" />' % (self.photo))
    
class ImageForFilterValue(BaseModel):
    title = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='images')
    Filter = models.ForeignKey(ValueForFilter, null=True, blank=True, on_delete=models.CASCADE)

    def image_tag(self):
        return mark_safe('<img src="/../../media/%s" width="150" height="150" />' % (self.photo))
    
######################################## TO DELETE ???
class Studio_type(BaseModel):
    size_in_persons = models.IntegerField() # Size of the studio (0-> artisan, 10-> really big (>100))
    
########################################
class Studio(BaseModel):
    size_in_persons = models.IntegerField(default=0, validators=[MaxValueValidator(10000), MinValueValidator(0)]) # Size of the studio (0-> artisan, 10-> really big (>100))
    type = models.ForeignKey(Studio_type, on_delete=models.CASCADE)
    url = models.URLField(null=True, blank=True)
    known_popularity = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)]) # Not used yet
    spotlight_count = models.IntegerField(default=0)
    they_have_made_it = models.IntegerField(default=0, validators=[MaxValueValidator(3), MinValueValidator(0)]) # 'They have made it! (1-> Yes, 2->Yes partly thanks to us, 3->Yes mostly thanks to us) 
    money_rating = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)]) 
    fully_rotten = models.BooleanField(default=False)
    in_hall_of_shame = models.BooleanField(default=False)

########################################
class Publisher(BaseModel):
    size_in_persons = models.IntegerField(default=0, validators=[MaxValueValidator(10000), MinValueValidator(0)]) # Size of the publisher (0-> artisan, 10-> really big (>100))
    url = models.URLField(null=True, blank=True)
    known_popularity = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)]) # Not used yet
    spotlight_count = models.IntegerField(default=0)
    they_have_made_it = models.IntegerField(default=0, validators=[MaxValueValidator(3), MinValueValidator(0)]) # They have made it! (1-> Yes, 2->Yes partly thanks to us, 3->Yes mostly thanks to us)
    money_rating = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    fully_rotten = models.BooleanField(default=False)
    in_hall_of_shame = models.BooleanField(default=False)

########################################
class Platform(BaseModel):
    pass
    
########################################
class Game_Category(BaseModel):
   pass
    
########################################
class Videogame_common(Entity):
    game_type = models.CharField(max_length=300)
    gameplay_rating = models.IntegerField(default=50, validators=[MaxValueValidator(100), MinValueValidator(0)])
    known_popularity = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    spotlight_count = models.IntegerField(default=0)
    in_the_spotlight = models.BooleanField(default=False)
    in_the_spotlight_since = models.DateTimeField(null=True, blank=True, editable=False)
    they_have_made_it = models.IntegerField(default=0, validators=[MaxValueValidator(3), MinValueValidator(0)]) # They have made it! (1-> Yes, 2->Yes partly thanks to us, 3->Yes mostly thanks to us)
    publishers =  models.ManyToManyField(Publisher)
    studios = models.ManyToManyField(Studio)
    platforms = models.ManyToManyField(Platform)
    categories = models.ManyToManyField(Game_Category)
    
# Inline
########################################
class Videogame_rating(BaseModel):
    for_platform = models.ForeignKey(Platform, on_delete=models.PROTECT)
    f2play = models.BooleanField(default=False)
    f2pay = models.BooleanField(default=False)
    gameplay_rating = models.IntegerField(default=50)
    money_rating = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    good_wo_iap = models.IntegerField(default=-1, validators=[MaxValueValidator(100), MinValueValidator(-1)])
    good_wo_ads = models.IntegerField(default=-1, validators=[MaxValueValidator(100), MinValueValidator(-1)])
    ads_supported = models.IntegerField(default=-1, validators=[MaxValueValidator(100), MinValueValidator(-1)])
    fully_rotten = models.BooleanField(default=False)
    would_be_good_if = models.TextField(max_length=1000, null=True, blank=True)
    could_be_good_if = models.TextField(max_length=1000, null=True, blank=True)
    use_psycho_tech = models.IntegerField(default=0)  
    Videogame_common = models.ForeignKey(Videogame_common, on_delete=models.CASCADE, null=True, blank=False)
    
    
# Sponsor too (like a studio, type+size of contribution? +url)
########################################
class Sponsor(BaseModel):
    url = models.URLField()
    sponsor_logo = models.ImageField()

    in_hall_of_shame = models.BooleanField(default=False)
    descriptionOfShame = models.TextField(max_length=1000)
    
class Company_group(Entity):
    company_logo = models.ImageField()
    
########################################
class Physical_shop(Entity):
    shop_type = models.CharField(max_length=300)
    ethical_rating = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    clarity_rating = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    spotlight_count = models.IntegerField(default=0)
    they_have_made_it = models.IntegerField(default=0, validators=[MaxValueValidator(3), MinValueValidator(0)]) # They have made it! (1-> Yes, 2->Yes partly thanks to us, 3->Yes mostly thanks to us)
    shop_logo = models.ImageField()
    group =  models.ManyToManyField(Company_group, blank=True)
    
########## Online Shop ##################
class Online_Shop(Entity):
    shop_type = models.CharField(max_length=300)
    ethical_rating = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    clarity_rating = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    spotlight_count = models.IntegerField(default=0)
    they_have_made_it = models.IntegerField(default=0, validators=[MaxValueValidator(3), MinValueValidator(0)]) # They have made it! (1-> Yes, 2->Yes partly thanks to us, 3->Yes mostly thanks to us)
    shop_logo = models.ImageField()
    group =  models.ManyToManyField(Company_group, blank=True)
      
########################################
class Links_to_shops(models.Model):
    link = models.URLField()
    identity = models.CharField(max_length=300)
    shop = models.ForeignKey(Online_Shop, on_delete=models.CASCADE, related_name="on_shop")
    for_Entity = models.ForeignKey(Entity, on_delete=models.CASCADE, null=True, blank=True)
    
class Software(Entity):
    software_type = models.CharField(max_length=300)
    ethical_rating = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    clarity_rating = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    heaviness = models.IntegerField(default=50, validators=[MaxValueValidator(100), MinValueValidator(0)])
    do_the_minimum = models.IntegerField(default=50, validators=[MaxValueValidator(100), MinValueValidator(0)])
    
    spotlight_count = models.IntegerField(default=0)
    they_have_made_it = models.IntegerField(default=0, validators=[MaxValueValidator(3), MinValueValidator(0)]) # They have made it! (1-> Yes, 2->Yes partly thanks to us, 3->Yes mostly thanks to us)
    
    publishers =  models.ManyToManyField(Publisher)
    studios = models.ManyToManyField(Studio)
    platforms = models.ManyToManyField(Platform)
    
#### Prefilled from Steam API, used to fetch a game ###############
class Entry_on_Steam(BaseModel):
    appid = models.IntegerField(null=False, blank=False)
    name = models.CharField(max_length=600)
    
class Entry_on_GooglePlay(BaseModel):
    appid = models.CharField(max_length=600, null=False, blank=False)
    name = models.CharField(max_length=600)
    
class Entry_on_AppleStore(BaseModel):
    appid = models.CharField(max_length=600, null=False, blank=False)
    name = models.CharField(max_length=600)
    
### Mirror tables to fetch stupidly all new entries
class New_Entry_on_Steam(BaseModel):
    appid = models.IntegerField(null=False, blank=False)
    name = models.CharField(max_length=600)
    
class New_Entry_on_GooglePlay(BaseModel):
    appid = models.CharField(max_length=600, null=False, blank=False)
    name = models.CharField(max_length=600)
    
class New_Entry_on_AppleStore(BaseModel):
    appid = models.CharField(max_length=600, null=False, blank=False)
    name = models.CharField(max_length=600)