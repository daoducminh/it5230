from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core import serializers
from django.db.models.functions import Now

from .views import LoginRequiredView
from .models import Menu, Dish, Menu_Dish
from utils.calories import bmr
import json
import random

calories_conf = [
    (-1, -1),
    (-1, 200),
    (200, 500),
    (500, 1000),
    (1000, 2000),
    (2000, -1)
]

LIMIT_DISH_FILTER = 10

class index(LoginRequiredView):
    def get(self, request):
        return self.execute(request)
    def post(self, request):
        return self.execute(request)
    def execute(self, request):
        # Menu.objects.all().delete()
        return render(request, 'menu/index.html', None)


class create(LoginRequiredView):
    def get(self, request):
        return self.execute(request)
    def post(self, request):
        return self.execute(request)
    def execute(self, request):
        user = request.user.user
        data = {}
        weight = user.weight
        height = user.height
        gender = user.gender
        diet_factor = user.diet_factor
        calories = bmr(weight, height, gender, 20, diet_factor)
        data['calories'] = calories
        data['calories_conf'] = calories_conf
        return render(request, 'menu/create.html', data)

class create_query(LoginRequiredView):
    def get(self, request):
        return self.execute(request)
    def post(self, request):
        # dishes = request.POST.getlist('dishes[]')
        content = {}
        content['dishes'] = json.loads(request.POST['dishes'])
        content['description'] = request.POST['description']
        content['limit'] = request.POST['limit']
        return self.execute(request, content)
    def execute(self, request, content):
        user = request.user.user
        menu = Menu(
            user=request.user,
            description=content['description'],
            mealtime=Now(),
            limit=content['limit'],
        )
        menu.save()
        dishes = content['dishes']
        for d in dishes:
            print(d)
            dish = Dish.objects.get(pk=d['dish_id'])
            m_d = Menu_Dish.objects.create(
                dish=dish,
                menu = menu,
                count=d['count']
            )
            m_d.save()
        return HttpResponseRedirect("/menu/")


class history(ListView):
    model = Menu
    paginate_by = 5
    context_object_name = "menus"
    template_name = "menu/history.html"
    def get_queryset(self):
        menus = Menu.objects.filter(user=self.request.user).order_by('-mealtime') 
        for menu in menus:
            dishes = menu.dishes.all()
            calories = sum((dish.calories for dish in dishes))
            menu.calories = calories
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

def query_filter_dish(request):
    calo_select = 0
    field = ""
    if (request.method == "POST"):
        calo_select = request.POST["calo_select"]
        field = request.POST["field"]
    calo_select = int(calo_select)
    calo_set = calories_conf[calo_select]
    query = Q()
    if calo_set[0] != -1:
        query = query & Q(calories__gte=calo_set[0])
    if calo_set[1] != -1:
        query = query & Q(calories__lte=calo_set[1])
    if len(field) != 0:
        query = query & (Q(dish_name__contains=field) | Q(description__contains=field))
    dishs = Dish.objects.filter(query)[:LIMIT_DISH_FILTER]

    json_dishs = serializers.serialize('json', dishs)
    return JsonResponse(json_dishs, content_type="text/json-comment-filtered", safe=False)