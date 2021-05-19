from django.contrib.auth.models import User as BaseUser
from django.contrib.postgres.fields import ArrayField
from django.db import models

from foods.validators import dish_image_path


class User(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    birthday = models.DateField()
    height = models.IntegerField()
    weight = models.IntegerField()
    gender = models.BooleanField()
    diet_factor = models.FloatField()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100)


class Dish(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    dish_name = models.CharField(max_length=200)
    description = ArrayField(base_field=models.CharField(max_length=10000), default=list)
    calories = models.IntegerField()
    is_public = models.BooleanField()
    image = models.ImageField(
        upload_to=dish_image_path
    )
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=0)
    total_time = models.IntegerField()
    image_url = models.CharField(max_length=1000, null=True)
    ingredients = ArrayField(base_field=models.CharField(max_length=10000), default=list)
    score = models.FloatField(default=0)
    review_number = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.dish_name

    class Meta:
        indexes = [
            models.Index(fields=['dish_name'], name='dish_name_idx'),
            models.Index(fields=['is_public'], name='is_public_idx'),
            models.Index(fields=['category'], name='category_idx'),
            models.Index(fields=['-created_at', '-updated_at'])
        ]


class Rating(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    score = models.IntegerField()
    comment = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.pk}-{self.dish.pk}'

    class Meta:
        unique_together = ('user', 'dish')
        indexes = [
            models.Index(fields=['-created_at', '-updated_at'])
        ]
