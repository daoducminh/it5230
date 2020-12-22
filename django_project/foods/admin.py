from django.contrib import admin

# Register your models here.
from .models import User, Dish

admin.site.register((User, Dish))
