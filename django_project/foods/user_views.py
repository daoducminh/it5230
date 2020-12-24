from django.db import transaction
from django.shortcuts import render, redirect
from django.views.generic.base import View

from .forms import UserForm, BaseUserForm
from .models import User
from .views import LoginRequiredView, UserUpdateView


# Testing purpose

class ProfileView(LoginRequiredView):
    def get(self, request):
        user_info = request.user.user
        context = {
            'height': user_info.height,
            'weight': user_info.weight,
            'gender': user_info.gender
        }
        return render(request, 'registration/profile.html', context)

    def post(self, request):
        height = request.POST['height']
        weight = request.POST['weight']
        gender = request.POST['gender']
        gender = True if gender == 'male' else False
        user_info = request.user.user
        user_info.height = height
        user_info.weight = weight
        user_info.gender = gender
        user_info.save()
        context = {
            'height': height,
            'weight': weight,
            'gender': gender,
            'message': 'Updated successfully'
        }
        return render(request, 'registration/profile.html', context)


class ProfileUpdate(UserUpdateView):
    # model = User
    # fields = ['height', 'weight', 'gender']
    form_class = UserForm
    queryset = User.objects.all()
    success_url = '/thanks/'


class RegisterView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            base_user_form = BaseUserForm()
            user_form = UserForm()
            return render(request, 'registration/register.html', {
                'user_form': user_form,
                'base_user_form': base_user_form
            })
        else:
            return redirect('account_profile')

    def post(self, request):
        if not request.user.is_authenticated:
            base_user_form = BaseUserForm(request.POST)
            user_form = UserForm(request.POST)
            if base_user_form.is_valid() and user_form.is_valid():
                with transaction.atomic():
                    base_user = base_user_form.save()
                    user = user_form.save(commit=False)
                    user.user = base_user
                    user.show_weight = True
                    user.show_height = True
                    user.show_email = True
                    user.show_gender = True
                    user.show_diet = True
                    user.show_phone = True
                    user.save()
                return redirect('login')
            else:
                return render(request, 'registration/register.html', {
                    'user_form': user_form,
                    'base_user_form': base_user_form
                })
        else:
            return redirect('account_profile')
