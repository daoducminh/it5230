# from django.contrib import admin

# # Register your models here.
# from .models import User, Dish

# admin.site.register((User, Dish))

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse


class Login(View):
    def get(self, request):
        return render(request, 'admin/dashboard.html')

    def post(self, request):
        return render(request, 'admin/dashboard.html')