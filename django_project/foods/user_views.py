from django.shortcuts import render

from .views import UserRequiredView


class ProfileView(UserRequiredView):
    def get(self, request):
        print(request.user)
        return render(request, 'registration/profile.html')


class TestView(UserRequiredView):
    def get(self, request):
        return render(request, 'index.html')
