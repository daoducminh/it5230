from django.forms import ModelForm, PasswordInput, CharField, NumberInput, CheckboxInput

from .constants.form_styles import *
from .models import Dish, User, BaseUser


class BaseUserForm(ModelForm):
    password1 = CharField(
        label='Input your password',
        max_length=50,
        widget=PasswordInput()
    )
    password2 = CharField(
        label='Input your password again',
        max_length=50,
        widget=PasswordInput()
    )

    class Meta:
        model = BaseUser
        fields = ['username', 'email', 'first_name', 'last_name']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['height', 'weight', 'gender', 'diet_factor']
        widgets = {
            'height': NumberInput(attrs={'class': FORM_CONTROL}),
            'weight': NumberInput(attrs={'class': FORM_CONTROL}),
            'gender': CheckboxInput(attrs={'class': FORM_CONTROL}),
            'diet_factor': NumberInput(attrs={'class': FORM_CONTROL}),
        }


class DishForm(ModelForm):
    class Meta:
        model = Dish
        exclude = ['user']
