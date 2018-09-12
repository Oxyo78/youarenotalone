from django.contrib import admin
from .models import Interest, UserProfile, City, News

admin.site.register(Interest)
admin.site.register(UserProfile)
admin.site.register(City)
admin.site.register(News)

# Register your models here.
