from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View


def index(request):
    context = {
        'app_name': 'Foods'
    }
    return render(request, 'index.html', context)


class UserRequiredView(LoginRequiredMixin, View):
    login_url = '/accounts/login'


class AdminRequiredView(LoginRequiredMixin, View):
    login_url = '/admins/login'
