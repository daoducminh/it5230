from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages

from foods.models import User as FoodsUser
from foods.models import Dish


class Login(View):
    def get(self, request):
        return render(request, 'admin/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            u = User.objects.get(username=username)
            if u.is_superuser and u.is_active:
                login(request, user)
                return redirect('/admin')
            else:
                messages.error(
                    request, 'Tài khoản của bạn không có quyền truy cập')
        else:
            messages.error(request, 'Sai tên đăng nhập hoặc mật khẩu')
        return render(request, 'admin/login.html')


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/admin/login')


class Index(LoginRequiredMixin, View):
    login_url = '/admin/login'

    def get(self, request):
        return render(request, 'admin/base.html')

    def post(self, request):
        return render(request, 'admin/base.html')


class UserManagement(LoginRequiredMixin, View):
    login_url = '/admin/login'

    def get(self, request):
        users = User.objects.all()
        foodsusers = FoodsUser.objects.all()
        context = {'users': users, 'foodsusers': foodsusers}
        return render(request, 'admin/user_management.html', context)

    def post(self, request):
        return render(request, 'admin/user_management.html')


class DishManagement(LoginRequiredMixin, View):
    login_url = '/admin/login'

    def get(self, request):
        dishes = Dish.objects.all()
        context = {'dishes': dishes}
        return render(request, 'admin/dish_management.html', context)

    def post(self, request):
        return render(request, 'admin/dish_management.html')