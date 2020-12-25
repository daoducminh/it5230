from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, CharField, NumberInput, CheckboxInput, EmailField, EmailInput

from .constants.form_styles import *
from .models import Dish, User


class BaseUserForm(UserCreationForm):
    email = EmailField(
        label='Email',
        widget=EmailInput(),
        max_length=50
    )
    first_name = CharField(
        label='First name',
        max_length=50
    )
    last_name = CharField(
        label='Last name',
        max_length=50
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        if commit:
            user.save()
        return user


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
