from django.contrib import admin

# Register your models here.
from .models import User, Recipe, Rating, Category, Menu

admin.site.register((User, Recipe, Rating, Category, Menu))
