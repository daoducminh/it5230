from django.forms.models import model_to_dict
from django.shortcuts import render, HttpResponse
from django.views.generic import View

from .models import Dish
from .views import UserRequiredView


class AllDishView(UserRequiredView):
    def get(self, request):
        dishes = Dish.objects.all()
        context = {'dishes': dishes}
        return render(request, 'foods/dishes.html', context)
    def post(self, request):
        dishes = Dish.objects.all()
        context = {'dishes': dishes}
        return render(request, 'foods/dishes.html', context)


class DishView(UserRequiredView):
    def get(self, request, dish_id):
        dish = Dish.objects.get(pk=dish_id)
        context = {'dish': dish}
        if dish.is_public or (request.user.is_authenticated and request.user.pk == dish.user_id):
            return render(request, 'foods/dish.html', context)
        else:
            return HttpResponse("Not authorized or not public")

    def post(self, request, dish_id):
        dish = Dish.objects.get(pk=dish_id)
        context = {'dish': dish}
        if dish.is_public or (request.user.is_authenticated and request.user.pk == dish.user_id):
            return render(request, 'foods/dish.html', context)
        else:
            return HttpResponse("Not authorized or not public")
