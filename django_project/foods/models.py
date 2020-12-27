from django.contrib.auth.models import User as BaseUser
from django.contrib.postgres import fields
from django.db import models

# Create your models here.
from django.urls import reverse


class User(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    birthday = models.DateField()
    height = models.IntegerField()
    weight = models.IntegerField()
    gender = models.BooleanField()
    diet_factor = models.FloatField()

    def __str__(self):
        return self.user.username

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(weight__gt=0), name='weight_gt_0'),
            models.CheckConstraint(check=models.Q(height__gt=100), name='height_gt_100'),
            models.CheckConstraint(check=models.Q(diet_factor__gt=0), name='diet_factor_gt_0')
        ]


class Dish(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    dish_name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    calories = models.IntegerField()
    is_public = models.BooleanField()
    ingredients = fields.ArrayField(
        models.CharField(max_length=50)
    )

    def __str__(self):
        return self.dish_name

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(calories__gt=0), name='calories_gt_0'),
        ]


class Rating(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    score = models.IntegerField()
    comment = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.pk}-{self.dish.pk}'

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(score__gt=0), name='score_gt_0'),
            models.CheckConstraint(check=models.Q(score__lte=5), name='score_lte_5'),
        ]
        unique_together = ('user', 'dish')
        ordering = ['-timestamp']


class Menu(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    mealtime = models.DateTimeField()
    limit = models.IntegerField()
    dishes = models.ManyToManyField(Dish, null=True, through="Menu_Dish")

    # calories it not necessary but db keep it in local, i am not able to fix it
    calories = models.IntegerField(default=0)

class Menu_Dish(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(count__gt=0), name="count_gt_0")
        ]