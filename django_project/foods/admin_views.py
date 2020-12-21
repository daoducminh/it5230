from django.shortcuts import render

from .views import AdminRequiredView


class HomeView(AdminRequiredView):
    def get(self, request):
        return render(request, 'admins/base.html')

    def post(self, request):
        return render(request, 'admins/base.html')


class UserManagementView(AdminRequiredView):
    def get(self, request):
        return render(request, 'admins/user_management.html')

    def post(self, request):
        return render(request, 'admins/user_management.html')


class DishManagementView(AdminRequiredView):
    def get(self, request):
        return render(request, 'admins/dish_management.html')

    def post(self, request):
        return render(request, 'admins/dish_management.html')
