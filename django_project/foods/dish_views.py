from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from .forms import DishForm, RatingForm
from .models import Dish, Rating
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


class AllRatingsView(View):
    def get(self, request, pk):
        dish = get_object_or_404(Dish, pk=pk)
        ratings = Rating.objects.filter(dish=dish)
        p = Paginator(ratings, 4)
        page = p.get_page(request.GET.get('page', 1))
        return render(request, 'ratings.html', {
            'page_obj': page
        })


class CreateRatingView(LoginRequiredView):
    def get(self, request, pk):
        get_object_or_404(Dish, pk=pk)
        return render(request, 'rating_form.html')

    def post(self, request, pk):
        dish = get_object_or_404(Dish, pk=pk)
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            try:
                rating = rating_form.save(False)
                rating.user = request.user
                rating.dish = dish
                rating.save()
                return render(request, 'rating_form.html', {
                    'message': 'Create successfully',
                    'rating': rating
                })
            except Exception as e:
                print(e)
                return render(request, 'rating_form.html', {
                    'errors': 'You have already rated this dish'
                })
        else:
            return render(request, 'rating_form.html', {
                'errors': rating_form.errors
            })


class UpdateRatingView(LoginRequiredView):
    def get(self, request, pk):
        dish = get_object_or_404(Dish, pk=pk)
        rating = get_object_or_404(Rating, user=request.user, dish=dish)
        return render(request, 'rating_form.html', {
            'rating': rating
        })

    def post(self, request, pk):
        dish = get_object_or_404(Dish, pk=pk)
        instance = get_object_or_404(Rating, user=request.user, dish=dish)
        rating_form = RatingForm(request.POST, instance=instance)
        if rating_form.is_valid():
            rating = rating_form.save()
            return render(request, 'rating_form.html', {
                'rating': rating,
                'message': 'Update successfully'
            })
        else:
            return render(request, 'rating_form.html', {
                'rating': instance,
                'errors': rating_form.errors
            })


class SearchDishView(View):
    def get(self, request):
        query = self.request.GET.get('search')
        dishes = Dish.objects.filter(dish_name__contains=query, is_public=True)
        if dishes:
            p = Paginator(dishes, 10)
            page = p.get_page(request.GET.get('page', 1))
            return render(request, 'dishes.html', {
                'page_obj': page
            })
        else:
            return render(request, 'dishes.html', {
                'error': 'No dish found'
            })