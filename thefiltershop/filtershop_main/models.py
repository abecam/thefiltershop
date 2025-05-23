from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.utils.safestring import mark_safe
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

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
    last_changed_by = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="%(app_label)s_%(class)s_all_editors")
    date_creation = models.DateTimeField("date creation", auto_now_add=True)
    last_update = models.DateTimeField("last updated", auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        abstract = True
        ordering = ['date_creation', 'name']
        indexes = [
            models.Index(fields=["name"])
        ]

class Filter(BaseModel):
    is_positive = models.BooleanField(default=False) # Fiters are mostly for bad things (too many IAPS, false Ads,... ) but could be positive too (educative, relaxing, ...)

    long_description = models.TextField(max_length=20000, null=True, blank=True)
    what_to_change = models.TextField(max_length=20000, null=True, blank=True)
    
class TypeOfRelationBetweenFilter(BaseModel):
    reverse_name = models.CharField(max_length=300, null=True, blank=True) # When the link if not both way and the relation if to to from.
    both_way = models.BooleanField(null=False, default=False) # False -> from to, True -> both way
    
# Relation to filter with a base model (i.e. name and description) so as to define the nature of the relation
class RelatedFilters(models.Model):
    from_filter = models.ForeignKey(Filter, on_delete=models.CASCADE, null=False, related_name="from_filter")
    to_filter = models.ForeignKey(Filter, on_delete=models.CASCADE, null=False, related_name="to_filter")
    with_type = models.ForeignKey(TypeOfRelationBetweenFilter, on_delete=models.PROTECT)
    
class TypeOfEntity(BaseModel):
    filters = models.ManyToManyField(Filter, blank=True)
            
class Tag(BaseModel):
    good_or_bad = models.IntegerField()
    parent_tag = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    
class Entity(BaseModel):
    # Ideally I would like an unique string id like type_product.publisher_name.studio_name.game_name
    # But I also don't think it should be a database ID (at least until the model is 100% set)
    headline = models.CharField(max_length=500, null=True, blank=True) # Line to show if on the front page
    url = models.URLField(null=True, blank=True)
    for_type = models.ForeignKey(TypeOfEntity, on_delete=models.PROTECT, related_name="%(app_label)s_%(class)s_related_type")
    general_rating = models.IntegerField(default=50, validators=[MaxValueValidator(100), MinValueValidator(0)])
    
    vignette = models.ImageField(default='none.jpg', upload_to='images', null=True, blank=False)
    
    hidden_full_cost = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)], verbose_name="Hidden full cost: 0 to 100",help_text="0 (none) to 50 (full price again (if not f2p)) to 80 (a lot more) to 100 (infinite, i.e. cannot be won whatever you spend)")
    description_hidden_full_cost = models.CharField(max_length=300, null=True, blank=True, verbose_name="You can give a custom description for the hidden full cost of this product",
                                                    help_text="A default text will be displayed otherwise, from 0 (none) to 100 (infinite: the product cannot be bought fully while it's possible to spend an infinite amoount of money.)") 
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
class ValueForFilter(models.Model):
    value = models.IntegerField(null=False, default=50, validators=[MaxValueValidator(100), MinValueValidator(0)]) # From 0 to 100
    filter = models.ForeignKey(Filter, on_delete=models.CASCADE, null=False)
    for_entity = models.ForeignKey(Entity, on_delete=models.CASCADE, null=False)

class Image(models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='images')
    Entity = models.ForeignKey(Entity, null=True, blank=True, on_delete=models.CASCADE)

    def image_tag(self):
        return mark_safe('<img src="/../../media/%s" width="150" height="150" />' % (self.photo))

class ImageForFilter(models.Model):
    title = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='images')
    Filter = models.ForeignKey(Filter, null=True, blank=True, on_delete=models.CASCADE)

    def image_tag(self):
        return mark_safe('<img src="/../../media/%s" width="150" height="150" />' % (self.photo))
    
class ImageForFilterValue(models.Model):
    title = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='images')
    Filter = models.ForeignKey(ValueForFilter, null=True, blank=True, on_delete=models.CASCADE)

    def image_tag(self):
        return mark_safe('<img src="/../../media/%s" width="150" height="150" />' % (self.photo))
    
########################################
class Studio(Entity):
    class SizeInPersons(models.TextChoices):
        ARTISAN = "AR", _("Artisan (5 persons or less)")
        INDIE = "IN", _("Indie (>5 persons, less than 20)")
        MEDIUM = "ME", _("Medium (>20, less than 50)")
        BIG = "BI", _("Big (>50 less than 200)")
        HUGE = "HU", _("Huge (>200)")
        
    size_of_studio = models.CharField(
        max_length=2,
        choices=SizeInPersons.choices,
        default=SizeInPersons.ARTISAN,
    )

    class TheyHaveMadeIt(models.TextChoices):
        NO = "NO", _("Not yet")
        YES = "YE", _("Yes")
        YES_WE_HELPED_A_BIT = "ME", _("Yes, and we helped a bit")
        YES_THANKS_TO_US = "MA", _("Yes, mostly thanks to us! Great!")
        
    they_have_made_it = models.CharField(
        max_length=2,
        choices=TheyHaveMadeIt.choices,
        default=TheyHaveMadeIt.NO,
    )
    
    known_popularity = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)]) # Not used yet
    spotlight_count = models.IntegerField(default=0)
    money_rating = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)]) 
    fully_rotten = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "A Studio"
        verbose_name_plural = "Studios"
        # The indexes are for the parent class Entity
        indexes = []

########################################
class Publisher(Entity):
    class SizeInPersons(models.TextChoices):
        ARTISAN = "AR", _("Artisan (5 persons or less)")
        INDIE = "IN", _("Indie (>5 persons, less than 20)")
        MEDIUM = "ME", _("Medium (>20, less than 50)")
        BIG = "BI", _("Big (>50 less than 200)")
        HUGE = "HU", _("Huge (>200)")
        
    size_of_publisher = models.CharField(
        max_length=2,
        choices=SizeInPersons.choices,
        default=SizeInPersons.ARTISAN,
    )
    
    class TheyHaveMadeIt(models.TextChoices):
        NO = "NO", _("Not yet")
        YES = "YE", _("Yes")
        YES_WE_HELPED_A_BIT = "ME", _("Yes, and we helped a bit")
        YES_THANKS_TO_US = "MA", _("Yes, mostly thanks to us! Great!")
        
    they_have_made_it = models.CharField(
        max_length=2,
        choices=TheyHaveMadeIt.choices,
        default=TheyHaveMadeIt.NO,
    )
    
    known_popularity = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)]) # Not used yet
    spotlight_count = models.IntegerField(default=0)
    money_rating = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    fully_rotten = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "A Publisher"
        verbose_name_plural = "Publishers"
        # The indexes are for the parent class Entity
        indexes = []

########################################
class Platform(BaseModel):
    pass
    
########################################
class Game_Category(BaseModel):
   class Meta:
        verbose_name = "Video Games' Category"
        verbose_name_plural = "Video Games' Categories"
    
########################################
class Videogame_common(Entity):
        
    class TheyHaveMadeIt(models.TextChoices):
        NO = "NO", _("Not yet")
        YES = "YE", _("Yes")
        YES_WE_HELPED_A_BIT = "ME", _("Yes, and we helped a bit")
        YES_THANKS_TO_US = "MA", _("Yes, mostly thanks to us! Great!")
        
    they_have_made_it = models.CharField(
        max_length=2,
        choices=TheyHaveMadeIt.choices,
        default=TheyHaveMadeIt.NO,
    )
    
    game_type = models.CharField(max_length=300)
    gameplay_rating = models.IntegerField(default=50, validators=[MaxValueValidator(100), MinValueValidator(0)])
    known_popularity = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    spotlight_count = models.IntegerField(default=0)
    in_the_spotlight = models.BooleanField(default=False)
    in_the_spotlight_since = models.DateTimeField(null=True, blank=True, editable=False)
    publishers =  models.ManyToManyField(Publisher)
    studios = models.ManyToManyField(Studio)
    platforms = models.ManyToManyField(Platform)
    categories = models.ManyToManyField(Game_Category)
    
    class Meta:
        verbose_name = "A Video Game"
        verbose_name_plural = "Video Games"
        # The indexes are for the parent class Entity
        indexes = []
    
# Inline
########################################
class Videogame_rating(BaseModel):
    name = models.CharField(max_length=300, null=True, blank=True)
    same_platform_alternative_shop = models.CharField(max_length=600, null=True, blank=True, verbose_name="If on the same platform but for a different shop with different conditions (i.e. F2P instead of premium), give the name of the shop")
    
    ''' Rating for a Video Game on a platform. It could be the same device on another shop, for instance sold as premium in one, but free with ads on another. As such, they have their own filters.'''
    # Should that be several platforms?
    for_platform = models.ForeignKey(Platform, on_delete=models.PROTECT)
    f2play = models.BooleanField(default=False)
    f2pay = models.BooleanField(default=False) # Should maybe move to a filter?
    # Ratings: higher is better.
    gameplay_rating = models.IntegerField(default=50)
    money_rating = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    good_wo_iap = models.IntegerField(default=-1, validators=[MaxValueValidator(100), MinValueValidator(-1)])
    good_wo_ads = models.IntegerField(default=-1, validators=[MaxValueValidator(100), MinValueValidator(-1)])
    ads_supported = models.IntegerField(default=-1, validators=[MaxValueValidator(100), MinValueValidator(-1)])
    fully_rotten = models.BooleanField(default=False)
    would_be_good_if = models.TextField(max_length=1000, null=True, blank=True)
    could_be_good_if = models.TextField(max_length=1000, null=True, blank=True)
    # here, lower is better (-1 is none)
    use_psycho_tech = models.IntegerField(default=-1, validators=[MaxValueValidator(100), MinValueValidator(-1)])  
    crapometer = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    Videogame_common = models.ForeignKey(Videogame_common, on_delete=models.CASCADE, null=True, blank=False)
    
    def __str__(self):
        if self.name:
            return self.name
        else:
            return "Not filled yet"
    
    class Meta:
        verbose_name = "Rating with filters for one platform"
        verbose_name_plural = "Ratings with filters by platforms"
    
class FiltersForAVideoGameRating(models.Model):
    ''' Many time the video games will be ok on a platform (generally PC, consoles and Mac) and not on another (mobiles). In that case the filters apply on the rating, which if for a specific platform '''
    value = models.IntegerField(null=False, default=50, validators=[MaxValueValidator(100), MinValueValidator(0)]) # From 0 to 100
    filter = models.ForeignKey(Filter, on_delete=models.CASCADE, null=False)
    for_rating = models.ForeignKey(Videogame_rating, on_delete=models.CASCADE, null=False)   
    
    verbose_name = "Filtered for this platform with"
    verbose_name_plural = "Applied filters for this platform"
    
# Sponsor too (like a studio, type+size of contribution? +url)
########################################
class Sponsor(BaseModel):
    url = models.URLField(null=True, blank=True)
    sponsor_logo = models.ImageField()

    in_hall_of_shame = models.BooleanField(default=False)
    descriptionOfShame = models.TextField(max_length=1000, null=True, blank=True)

    def save(self, *args, **kwargs):
        # save the profile first
        super().save(*args, **kwargs)

        # resize the image
        img = PIL.Image.open(self.sponsor_logo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            # create a thumbnail
            img.thumbnail(output_size)
            # overwrite the larger image
            img.save(self.sponsor_logo.path)
    
class Company_group(Entity):
    company_logo = models.ImageField()
    
    class Meta:
        # The indexes are for the parent class Entity
        indexes = []
    
## Sponsors and contributors can suggest games
class Recommended_Games_By_Sponsor(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, null=False)
    game = models.ForeignKey(Videogame_common, on_delete=models.CASCADE, null=False)
    review_txt = models.TextField(max_length=10000, null=True, blank=True)
    note = models.IntegerField(null=False, default=5, validators=[MaxValueValidator(5), MinValueValidator(0)]) # From 0 to 5 stars
    

########################################
class Physical_shop(Entity):
    class SizeInPersons(models.TextChoices):
        ARTISAN = "AR", _("Artisan (5 persons or less)")
        INDIE = "IN", _("Indie (>5 persons, less than 20)")
        MEDIUM = "ME", _("Medium (>20, less than 50)")
        BIG = "BI", _("Big (>50 less than 200)")
        HUGE = "HU", _("Huge (>200)")
        
    size_of_shop = models.CharField(
        max_length=2,
        choices=SizeInPersons.choices,
        default=SizeInPersons.ARTISAN,
    )
    
    class TheyHaveMadeIt(models.TextChoices):
        NO = "NO", _("Not yet")
        YES = "YE", _("Yes")
        YES_WE_HELPED_A_BIT = "ME", _("Yes, and we helped a bit")
        YES_THANKS_TO_US = "MA", _("Yes, mostly thanks to us! Great!")
        
    they_have_made_it = models.CharField(
        max_length=2,
        choices=TheyHaveMadeIt.choices,
        default=TheyHaveMadeIt.NO,
    )
    
    shop_type = models.CharField(max_length=300)
    ethical_rating = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    clarity_rating = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    spotlight_count = models.IntegerField(default=0)
    in_the_spotlight = models.BooleanField(default=False)
    in_the_spotlight_since = models.DateTimeField(null=True, blank=True, editable=False)
    group =  models.ManyToManyField(Company_group, blank=True)
    
    class Meta:
        # The indexes are for the parent class Entity
        indexes = []
    
########## Online Shop ##################
class Online_Shop(Entity):
    class SizeInPersons(models.TextChoices):
        ARTISAN = "AR", _("Artisan (5 persons or less)")
        INDIE = "IN", _("Indie (>5 persons, less than 20)")
        MEDIUM = "ME", _("Medium (>20, less than 50)")
        BIG = "BI", _("Big (>50 less than 200)")
        HUGE = "HU", _("Huge (>200)")
        
    size_of_shop = models.CharField(
        max_length=2,
        choices=SizeInPersons.choices,
        default=SizeInPersons.ARTISAN,
    )
    
    class TheyHaveMadeIt(models.TextChoices):
        NO = "NO", _("Not yet")
        YES = "YE", _("Yes")
        YES_WE_HELPED_A_BIT = "ME", _("Yes, and we helped a bit")
        YES_THANKS_TO_US = "MA", _("Yes, mostly thanks to us! Great!")
        
    they_have_made_it = models.CharField(
        max_length=2,
        choices=TheyHaveMadeIt.choices,
        default=TheyHaveMadeIt.NO,
    )
    
    shop_type = models.CharField(max_length=300)
    ethical_rating = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    clarity_rating = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    spotlight_count = models.IntegerField(default=0)
    in_the_spotlight = models.BooleanField(default=False)
    in_the_spotlight_since = models.DateTimeField(null=True, blank=True, editable=False)
    group =  models.ManyToManyField(Company_group, blank=True)
    
    class Meta:
        # The indexes are for the parent class Entity
        indexes = []
      
class Profile(BaseModel):
    class ContributorLevel(models.TextChoices):
        REGULAR = "RE", _("Regular user")
        SUPPORTER = "SU", _("Supporter")
        SUPER_SUPPORTER = "SSU", _("Super Supporter")
        CURATOR = "CUR", _("Curator")
        
    contribution_level = models.CharField(
        max_length=3,
        choices=ContributorLevel.choices,
        default=ContributorLevel.REGULAR,
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    number_of_contrib = models.IntegerField(default=0) # Incremented when something is updated by the user.
    full_name = models.CharField(max_length=300)
    biography = models.TextField(max_length=3000)
    curating_fields = models.ManyToManyField(TypeOfEntity, blank=True)
    nb_of_articles = models.IntegerField(editable=False, default=0)
    
    avatar = models.ImageField(
        default='avatar.jpg', # default avatar
        upload_to='profile_avatars' # dir to store the image
    )

    recommended_games = models.ManyToManyField(Videogame_common)

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

## Contributors review are in the profile, but they can also review
## TODO: In the admin interface, make it as easy as possible to propagate the review to Steam.
class Review(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False)
    game = models.ForeignKey(Videogame_common, on_delete=models.CASCADE, null=False)
    review_txt = models.TextField(max_length=10000, null=True, blank=True)
    note = models.IntegerField(null=False, default=5, validators=[MaxValueValidator(5), MinValueValidator(-5)]) # From -5 to 5 stars
    
########################################
class Links_to_shops(models.Model):
    link = models.URLField()
    identity = models.CharField(max_length=300)
    shop = models.ForeignKey(Online_Shop, on_delete=models.CASCADE, related_name="on_shop")
    for_Entity = models.ForeignKey(Entity, on_delete=models.CASCADE, null=True, blank=True)
    
class Software(Entity):
    class TheyHaveMadeIt(models.TextChoices):
        NO = "NO", _("Not yet")
        YES = "YE", _("Yes")
        YES_WE_HELPED_A_BIT = "ME", _("Yes, and we helped a bit")
        YES_THANKS_TO_US = "MA", _("Yes, mostly thanks to us! Great!")
        
    they_have_made_it = models.CharField(
        max_length=2,
        choices=TheyHaveMadeIt.choices,
        default=TheyHaveMadeIt.NO,
    )
    
    software_type = models.CharField(max_length=300)
    ethical_rating = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    
    spotlight_count = models.IntegerField(default=0)
    in_the_spotlight = models.BooleanField(default=False)
    in_the_spotlight_since = models.DateTimeField(null=True, blank=True, editable=False)
    
    publishers =  models.ManyToManyField(Publisher)
    studios = models.ManyToManyField(Studio)
    platforms = models.ManyToManyField(Platform)
    
    class Meta:
        # The indexes are for the parent class Entity
        indexes = []
    
#### Prefilled from Steam API, used to fetch a game ###############
class Entry_on_Steam(models.Model):
    appid = models.IntegerField(null=False, blank=False)
    name = models.CharField(max_length=600)
    
class Entry_on_GooglePlay(models.Model):
    appid = models.CharField(max_length=600, null=False, blank=False)
    name = models.CharField(max_length=600)
    
class Entry_on_AppleStore(models.Model):
    appid = models.CharField(max_length=600, null=False, blank=False)
    name = models.CharField(max_length=600)
    
### Mirror tables to fetch stupidly all new entries
class New_Entry_on_Steam(models.Model):
    appid = models.IntegerField(null=False, blank=False)
    name = models.CharField(max_length=600)
    
class New_Entry_on_GooglePlay(models.Model):
    appid = models.CharField(max_length=600, null=False, blank=False)
    name = models.CharField(max_length=600)
    
class New_Entry_on_AppleStore(models.Model):
    appid = models.CharField(max_length=600, null=False, blank=False)
    name = models.CharField(max_length=600)
    
class AllEndStringFromSteam(models.Model):
    name = models.CharField(max_length=300)