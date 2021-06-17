from django.contrib.auth.models import User as BaseUser
from django.contrib.postgres.fields import ArrayField
from django.db import models

from foods.validators import image_path


class User(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    birthday = models.DateField()
    gender = models.BooleanField()
    image = models.ImageField(
        upload_to=image_path
    )
    image_url = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100)


class Recipe(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    recipe_name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    directions = ArrayField(base_field=models.CharField(max_length=10000), default=list)
    calories = models.IntegerField()
    image = models.ImageField(
        upload_to=image_path
    )
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=0)
    total_time = models.IntegerField()
    image_url = models.CharField(max_length=1000, null=True)
    ingredients = ArrayField(base_field=models.CharField(max_length=10000), default=list)
    score = models.FloatField(default=0)
    review_number = models.IntegerField(default=0)
    suggested = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.recipe_name

    class Meta:
        indexes = [
            models.Index(fields=['recipe_name'], name='recipe_name_idx'),
            models.Index(fields=['category'], name='category_idx'),
            models.Index(fields=['-created_at', '-updated_at', '-review_number', '-score'])
        ]


class Rating(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    score = models.IntegerField()
    comment = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.pk}-{self.recipe.pk}'

    class Meta:
        unique_together = ('user', 'recipe')
        indexes = [
            models.Index(fields=['-created_at', '-updated_at'])
        ]


class Menu(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    menu_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    recipes = models.ManyToManyField(Recipe)
    score = models.FloatField(default=0)
    review_number = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MenuRating(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    score = models.IntegerField()
    comment = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
