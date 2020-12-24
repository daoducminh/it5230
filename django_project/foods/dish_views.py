from django.forms.models import model_to_dict
from django.shortcuts import render

from .forms import DishForm
from .models import Dish
from .views import LoginRequiredView, SelfUpdateView, SelfDeleteView


class AllDishView(LoginRequiredView):
    def get(self, request):
        return render(request, '')


class DishView(LoginRequiredView):
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


class UserUpdateDishView(SelfUpdateView):
    form_class = DishForm
    queryset = Dish.objects.all()
    success_url = '/thanks/'


class UserDeleteDishView(SelfDeleteView):
    model = Dish
    success_url = '/thanks/'
