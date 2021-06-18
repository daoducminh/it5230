from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View

from .forms import UserForm, BaseUserForm
from .i18n.en import *
from .models import Recipe, Menu
from .views import LoginRequiredView, AdminOnlyView


class UpdateProfileView(LoginRequiredView):
    def get(self, request):
        user = request.user.user
        return render(request, 'registration/profile.html', {
            'form': user
        })

    def post(self, request):
        user_info = request.user.user
        user_form = UserForm(request.POST, instance=user_info)
        if user_form.is_valid():
            user = user_form.save(False)
            user.save()
            messages.success(request, PROFILE_UPDATED)
            return render(request, 'registration/profile.html', {
                'form': user
            })
        else:
            messages.error(request, user_form.errors)
            return render(request, 'registration/profile.html', {
                'form': user_info
            })


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
                    user.save()
                    messages.success(request, REGISTER_SUCCESS)
                return redirect('login')
            else:
                if base_user_form.errors:
                    messages.error(request, base_user_form.errors)
                if user_form.errors:
                    messages.error(request, user_form.errors)
                return render(request, 'registration/register.html', {
                    'user_form': user_form,
                    'base_user_form': base_user_form
                })
        else:
            return redirect('account_profile')


class UpdateActivationView(AdminOnlyView):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user.is_active:
            messages.success(request, DEACTIVATE_SUCCESS)
        else:
            messages.success(request, ACTIVATE_SUCCESS)
        user.is_active = not user.is_active
        user.save()
        return redirect('profile_detail', pk=pk)


class ProfileView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        recipes = Recipe.objects.filter(user=user).order_by('-review_number', '-score')
        menus = Menu.objects.filter(user=user).order_by('-review_number', '-score')
        return render(request, 'profile.html', {
            'user': user,
            'recipes': recipes,
            'menus': menus
        })
