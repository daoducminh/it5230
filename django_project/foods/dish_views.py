from django.forms.models import model_to_dict
from django.shortcuts import render
from django.views.generic import View

from .models import Dish
from .views import UserRequiredView


class AllDishView(UserRequiredView):
    def get(self, request):
        return render(request, '')


class DishView(UserRequiredView):
    def get(self, request, dish_id):
        dish = Dish.objects.get(pk=dish_id)
        if dish.is_public or (request.user.is_authenticated and request.user.pk == dish.user_id):
            return render(request, '', model_to_dict(dish))
        else:
            # Not authorized or not public
            pass

    def post(self, request, dish_id):
        dish = Dish.objects.get(pk=dish_id)
        if dish.is_public or (request.user.is_authenticated and request.user.pk == dish.user_id):
            return render(request, '', model_to_dict(dish))
        else:
            # Not authorized or not public
            pass
