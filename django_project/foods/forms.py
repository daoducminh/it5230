from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, CharField, EmailField, EmailInput, ImageField, DateField, BooleanField

from .models import Recipe, User, Rating, MenuRating, Category


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
    image = ImageField(required=False)
    image_url = CharField(required=False)
    birthday = DateField(required=False)
    gender = BooleanField(required=False)

    class Meta:
        model = User
        fields = ('birthday', 'gender', 'image', 'image_url')


class RecipeForm(ModelForm):
    image = ImageField(required=False)
    image_url = CharField(required=False)

    class Meta:
        model = Recipe
        exclude = ('user', 'created_at', 'updated_at', 'score', 'review_number', 'tsv')


class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ('score', 'comment')


class MenuRatingForm(ModelForm):
    class Meta:
        model = MenuRating
        fields = ('score', 'comment')


class CategoryForm(ModelForm):
    short_name = CharField(required=False)

    class Meta:
        model = Category
        fields = ('title', 'short_name')
