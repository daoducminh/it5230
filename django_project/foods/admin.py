# from django.contrib import admin

# # Register your models here.
# from .models import User, Dish

# admin.site.register((User, Dish))

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse


class Index(View):
    def get(self, request):
        return render(request, 'admin/base.html')

    def post(self, request):
        return render(request, 'admin/base.html')


class UserManagement(View):
    def get(self, request):
        return render(request, 'admin/user_management.html')

    def post(self, request):
        return render(request, 'admin/user_management.html')


class DishManagement(View):
    def get(self, request):
        return render(request, 'admin/dish_management.html')

    def post(self, request):
        return render(request, 'admin/dish_management.html')