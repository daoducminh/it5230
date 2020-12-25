from django.shortcuts import render, redirect

from .forms import DishForm
from .models import Dish
from .views import SelfUpdateView, SelfDeleteView, UserListView, UserDetailView, AdminListView, AdminDetailView, \
    LoginRequiredView


class AdminAllDishView(AdminListView):
    model = Dish
    template_name = "admins/dishes.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AdminDishView(AdminDetailView):
    model = Dish
    template_name = 'admins/dish.html'

    def get_context_data(self, **kwarg):
        context = super().get_context_data(**kwarg)
        return context


class UserDishView(UserDetailView):
    model = Dish
    template_name = 'users/dish.html'
    queryset = Dish.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_context_data(self, **kwarg):
        context = super().get_context_data(**kwarg)
        return context


class UserAllDishView(UserListView):
    model = Dish
    template_name = 'users/dishes.html'
    queryset = Dish.objects.all()
    paginate_by = 10

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_context_data(self, **kwarg):
        context = super().get_context_data(**kwarg)
        return context


class UpdateDishView(SelfUpdateView):
    form_class = DishForm
    queryset = Dish.objects.all()
    success_url = '/thanks/'


class DeleteDishView(SelfDeleteView):
    model = Dish
    success_url = '/thanks/'


class CreateDishView(LoginRequiredView):
    def get(self, request):
        return render(request, 'foods/dish_add.html')

    def post(self, request):
        dish_form = DishForm(request.POST)
        if dish_form.is_valid():
            dish = dish_form.save(False)
            dish.user = request.user
            dish.save()
            return redirect('thanks')
        else:
            return render(request, 'foods/dish_add.html', {
                'errors': dish_form.errors
            })
