from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class City(models.Model):
    """ List of citys """
    cityName = models.CharField(max_length=45)
    postalCode = models.IntegerField()
    coordinateLng = models.DecimalField(max_digits=12, decimal_places=10)
    coordinateLat = models.DecimalField(max_digits=12, decimal_places=10)

    def __str__(self):
        return self.cityName


# Interest table
class Interest(models.Model):
    """ List of interests """
    interestName = models.CharField(max_length=35)
     
    def __str__(self):
        return self.interestName


# Add more information to the user
class UserProfile(models.Model):
    """ User profile extension """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, null=True)
    interestId = models.ManyToManyField(Interest, related_name="interestUser")
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class News(models.Model):
    """ News on main pages """
    title = models.CharField(max_length=50)
    content = models.TextField()
    dateSave= models.DateField(auto_now_add=True)