from django.shortcuts import render
from django.views.generic import View

from django.http import HttpRequest


class LoginView(View):
    def get(self, request, name):
        return render(request, 'users/login.html', {
            'method': 'GET',
            'name': name
        })

    def post(self, request, name):
        return render(request, 'users/profile.html', {
            'method': 'POST',
            'name': name
        })


# def login(request: HttpRequest):
#     if request.method == HttpRequest.GET:
#         return render(request, 'users/login.html')
