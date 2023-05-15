from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from PIL import Image

class User(AbstractUser):
    pass

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=300)
   
    nb_of_articles = models.IntegerField(editable=False, default=0)
    
    avatar = models.ImageField(
        default='avatar.jpg', # default avatar
        upload_to='profile_avatars' # dir to store the image
    )
    
    date_creation = models.DateTimeField("date creation", auto_now_add=True)
    last_update = models.DateTimeField("last updated", auto_now=True)
    
    def __str__(self):
        return f'{self.user.full_name} Profile'
    
    def save(self, *args, **kwargs):
        # save the profile first
        super().save(*args, **kwargs)

        # resize the image
        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            # create a thumbnail
            img.thumbnail(output_size)
            # overwrite the larger image
            img.save(self.avatar.path)
    
class Tag(models.Model):
    name = models.CharField(max_length=300)
    good_or_bad = models.IntegerField()
    parent_tag = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, 
                                    verbose_name=('Created by'), editable=False, null=True, blank=True)
    date_creation = models.DateTimeField("date creation", auto_now_add=True)
    last_update = models.DateTimeField("last updated", auto_now=True)
    
    def __str__(self):
        return self.name
    

########################################
class Shop(models.Model):
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=4000)
    url = models.CharField(max_length=200)
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
    description = models.CharField(max_length=1000)
    link = models.CharField(max_length=300)
    identity = models.CharField(max_length=300)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL,
                                    verbose_name=('Created by'), editable=False, null=True, blank=True)
    date_creation = models.DateTimeField("date creation", auto_now_add=True)
    last_update = models.DateTimeField("last updated", auto_now=True)
    
    def __str__(self):
        return self.name

class Entity(models.Model):
    # Ideally I would like an unique string id like type_product.publisher_name.studio_name.game_name
    # But I also don't think it should be a database ID (at least until the model is 100% set)
    name = models.CharField(max_length=300)
    type = models.CharField(max_length=100)
    general_rating = models.IntegerField()
    ethical_money_rating = models.IntegerField()
    ethical_moral_rating = models.IntegerField()
    ethical_marketing_rating = models.IntegerField()
    ethical_educational_rating = models.IntegerField()
    cheating_review = models.IntegerField()
    cheating_ads = models.IntegerField()
    insulting_ads = models.IntegerField()
    misleading_ads = models.IntegerField()
    desc_cheating_ads = models.CharField(max_length=1000)
    desc_insulting_ads = models.CharField(max_length=1000)
    desc_misleading_ads = models.CharField(max_length=1000)
    hidden_full_cost = models.IntegerField()
    crapometer = models.IntegerField()
    description = models.CharField(max_length=4000)
    in_hall_of_shame = models.BooleanField()
    Links_to_shops = models.ForeignKey(Links_to_shops, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(Tag)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL,
                                    verbose_name=('Created by'), editable=False, null=True, blank=True)
    date_creation = models.DateTimeField("date creation", auto_now_add=True)
    last_update = models.DateTimeField("last updated", auto_now=True)
    
    def __str__(self):
        return self.name



########################################
class Studio_type(models.Model):
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=1000)
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
    they_have_made_it = models.IntegerField() # 'They have made it! (1-> Yes, 2->Yes partly thanks to us, 3->Yes mostly thanks to us) 
    money_rating = models.IntegerField() 
    fully_rotten = models.BooleanField()
    in_hall_of_shame = models.BooleanField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL,
                                    verbose_name=('Created by'), editable=False, null=True, blank=True)
    date_creation = models.DateTimeField("date creation", auto_now_add=True)
    last_update = models.DateTimeField("last updated", auto_now=True)
    
    def __str__(self):
        return self.name_of_studio

########################################
class Publisher(models.Model):
    name = models.CharField(max_length=300)
    size = models.IntegerField() # Size of the publisher (0-> artisan, 10-> really big (>100))
    they_have_made_it = models.IntegerField() # They have made it! (1-> Yes, 2->Yes partly thanks to us, 3->Yes mostly thanks to us)
    money_rating = models.IntegerField()
    fully_rotten = models.BooleanField()
    in_hall_of_shame = models.BooleanField()
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
    gameplay_rating = models.IntegerField()
    for_entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    they_have_made_it = models.IntegerField() # They have made it! (1-> Yes, 2->Yes partly thanks to us, 3->Yes mostly thanks to us)
    publishers =  models.ManyToManyField(Publisher)
    studios = models.ManyToManyField(Studio)
    platforms = models.ManyToManyField(Platform)
    created_by = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="videogame_common")
    date_creation = models.DateTimeField("date creation", auto_now_add=True)
    last_update = models.DateTimeField("last updated", auto_now=True)
    
########################################
class Videogame_rating(models.Model):
    f2play = models.BooleanField()
    f2pay = models.BooleanField()
    gameplay_rating = models.IntegerField()
    money_rating = models.IntegerField()
    good_wo_iap = models.IntegerField()
    good_wo_ads = models.IntegerField()
    ads_supported = models.IntegerField()
    fully_rotten = models.BooleanField()
    would_be_good_if = models.CharField(max_length=1000)
    could_be_good_if = models.CharField(max_length=1000)
    use_psycho_tech = models.IntegerField()  
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
    url = models.CharField(max_length=300)
    description = models.CharField(max_length=1000)
    image = description = models.ImageField

    in_hall_of_shame = models.BooleanField()
    descriptionOfShame = models.CharField(max_length=1000)
    created_by = models.ForeignKey(Person, on_delete=models.CASCADE)
    date_creation = models.DateTimeField("date creation", auto_now_add=True)
    last_update = models.DateTimeField("last updated", auto_now=True)
    
    def __str__(self):
        return self.name_of_studio