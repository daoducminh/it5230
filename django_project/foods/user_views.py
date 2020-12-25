from django.db import transaction
from django.shortcuts import render, redirect
from django.views.generic.base import View

from .forms import UserForm, BaseUserForm
from .views import LoginRequiredView


# Testing purpose

class UpdateProfileView(LoginRequiredView):
    def get(self, request):
        user = request.user.user
        return render(request, 'registration/profile.html', {
            'form': user
        })

    def post(self, request):
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            return render(request, 'registration/profile.html', {
                'form': user
            })
        else:
            return render(request, 'registration/profile.html', {
                'form': request.user.user,
                'errors': user_form.errors
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
                return redirect('login')
            else:
                return render(request, 'registration/register.html', {
                    'user_form': user_form,
                    'base_user_form': base_user_form
                })
        else:
            return redirect('account_profile')
