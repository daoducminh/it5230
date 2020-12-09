from django.db import models
from django.contrib.auth.models import User as BaseUser
from django.contrib.postgres import fields


# Create your models here.
class User(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    height = models.IntegerField()
    weight = models.IntegerField()
    fullname = models.CharField(max_length=50)
    gender = models.BooleanField()
    diet_factor = models.FloatField()
    phone = models.CharField(max_length=50)
    favorites = models.CharField(max_length=100)
    show_gender = models.BooleanField()
    show_phone = models.BooleanField()
    show_email = models.BooleanField()
    show_height = models.BooleanField()
    show_weight = models.BooleanField()
    show_diet = models.BooleanField()


class Dish(models.Model):
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    dish_name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    calories = models.IntegerField()
    is_public = models.BooleanField()
    ingredients = fields.ArrayField(
        models.CharField(max_length=50)
    )
    class Meta:
        constraints=[]


class Rating(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    dish_id = models.ForeignKey(Dish, on_delete=models.CASCADE)
    score = models.FloatField()
    comment = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)


class Menu(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    mealtime = models.DateTimeField()
    limit = models.IntegerField()
    dishes = models.ManyToManyField(Dish)
