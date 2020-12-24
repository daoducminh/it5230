from django.forms import ModelForm, NumberInput

from .models import Dish, User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['height', 'weight', 'gender']
        widgets = {
            'height': NumberInput(attrs={'class': 'btn'})
        }


class DishForm(ModelForm):
    class Meta:
        model = Dish
        exclude = ['user']
