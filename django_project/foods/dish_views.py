from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .forms import DishForm
from .models import Dish
from .views import LoginRequiredView, SelfUpdateView


class AdminAllDishView(LoginRequiredView, ListView):
    model = Dish
    template_name = "admins/admin_dishes.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AdminDishView(LoginRequiredView, DetailView):
    model = Dish
    template_name = 'admins/admin_dish.html'

    def get_context_data(self, **kwarg):
        context = super().get_context_data(**kwarg)
        return context


# class DishView(LoginRequiredView):
#     def get(self, request, dish_id):
#         dish = Dish.objects.get(pk=dish_id)
#         context = {'dish': dish}
#         if dish.is_public or (request.user.is_authenticated and request.user.pk == dish.user_id):
#             return render(request, 'foods/dish.html', context)
#         else:
#             return HttpResponse("Not authorized or not public")

#     def post(self, request, dish_id):
#         dish = Dish.objects.get(pk=dish_id)
#         context = {'dish': dish}
#         if dish.is_public or (request.user.is_authenticated and request.user.pk == dish.user_id):
#             return render(request, 'foods/dish.html', context)
#         else:
#             return HttpResponse("Not authorized or not public")


class UpdateDishView(SelfUpdateView):
    form_class = DishForm
    queryset = Dish.objects.all()
    success_url = '/thanks/'
