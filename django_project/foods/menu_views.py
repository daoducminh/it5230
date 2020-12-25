from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView

from .views import LoginRequiredView
from .models import Menu
import json


class index(LoginRequiredView):
    def get(self, request):
        return self.execute(request)
    def post(self, request):
        return self.execute(request)
    def execute(self, request):
        return render(request, 'menu/index.html', None)


class create(LoginRequiredView):
    def get(self, request):
        return self.execute(request)
    def post(self, request):
        return self.execute(request)
    def execute(self, request):
        user = request.user.user
        return render(request, 'menu/create.html')


class history(ListView):
    model = Menu
    paginate_by = 5
    context_object_name = "menus"
    template_name = "menu/history.html"
    def get_queryset(self):
        menus = Menu.objects.filter(user=self.request.user).order_by('-mealtime') 
        print(len(menus), "##")
        return menus
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["xxx"] = "Toi la toi =))"
        return context
    
    # def get(self, request):
    #     return self.execute(request)
    # def post(self, request):
    #     return self.execute(request)
    # def execute(self, request):
    #     user = request.user.user
    #     user_id = user.id
    #     menus = Menu.objects.filter(user = request.user)
    #     print(menus.values())
    #     # for m in menus:
    #     #     dishs = m.dishes.all()
    #     #     for d in dishs:
    #     #         print(d.id, d.dish_name, d.description, d.calories)
    #     return HttpResponse("Menu History")


class update(LoginRequiredView):
    def get(self, request):
        return self.execute(request)
    def post(self, request):
        return self.execute(request)
    def execute(self, request):
        return HttpResponse("Menu Update")


class delete(LoginRequiredView):
    def get(self, request):
        return self.execute(request)
    def post(self, request):
        return self.execute(request)
    def execute(self, request):
        return HttpResponse("Menu Delete")
