from django.db import models
from django.contrib.auth.models import User

# Add more information to the user
class User_info(models.Model):
    coordinate_lng = models.DecimalField(max_digits=9, decimal_places=6)
    coordinate_lat = models.DecimalField(max_digits=9, decimal_places=6)
    picture = models.ImageField()
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
     
    def __str__(self):
        return self.coordinate_lng, self.coordinate_lat

# Interest table
class Interest(models.Model):
    interest_name = models.CharField(max_length=35, unique=True)
     
    def __str__(self):
        return self.interest_name


class User_interest(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    interest_id = models.OneToOneField(Interest, on_delete=models.CASCADE)
