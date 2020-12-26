from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import View

from .forms import DishForm, RatingForm
from .i18n.vi import *
from .models import Dish, Rating
from .views import SelfUpdateView, SelfDeleteView, UserListView, AdminDetailView, \
    LoginRequiredView, UserOnlyView, AdminOnlyView


class AdminAllDishView(AdminOnlyView):
    def get(self, request, pk):
        dish = get_object_or_404(Dish, pk=pk, user=request.user)
        ratings = Rating.objects.filter(dish=dish)
        p = Paginator(ratings, 5)
        page = p.get_page(request.GET.get('page', 1))
        return render(request, 'users/dish.html', {
            'object': dish,
            'page_obj': page
        })


class AdminDishView(AdminDetailView):
    model = Dish
    template_name = 'admins/dish.html'

    def get_context_data(self, **kwarg):
        context = super().get_context_data(**kwarg)
        return context


class UserDishView(UserOnlyView):
    def get(self, request, pk):
        dish = get_object_or_404(Dish, pk=pk, user=request.user)
        ratings = Rating.objects.filter(dish=dish)
        p = Paginator(ratings, 5)
        page = p.get_page(request.GET.get('page', 1))
        return render(request, 'users/dish.html', {
            'object': dish,
            'page_obj': page
        })


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

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse('admin_dish_detail', kwargs={'pk': self.object.pk})
        else:
            return reverse('user_dish_detail', kwargs={'pk': self.object.pk})


class DeleteDishView(SelfDeleteView):
    model = Dish

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse('admin_all_dishes', kwargs={'pk': self.object.pk})
        else:
            return reverse('user_all_dishes', kwargs={'pk': self.object.pk})


class CreateDishView(LoginRequiredView):
    def get(self, request):
        return render(request, 'foods/dish_add.html')

    def post(self, request):
        dish_form = DishForm(request.POST)
        if dish_form.is_valid():
            dish = dish_form.save(False)
            dish.user = request.user
            dish.save()
            if request.user.is_staff:
                return redirect('admin_all_dishes', {
                    'message': DISH_CREATED
                })
            else:
                return redirect('user_all_dishes', {
                    'message': DISH_CREATED
                })
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
                    'message': RATE_CREATED,
                    'rating': rating
                })
            except Exception as e:
                print(e)
                return render(request, 'rating_form.html', {
                    'errors': RATE_DUPLICATED
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
                'message': RATE_UPDATED
            })
        else:
            return render(request, 'rating_form.html', {
                'rating': instance,
                'errors': rating_form.errors
            })


class DishDetailView(View):
    def get(self, request, pk):
        dish = get_object_or_404(Dish, pk=pk)
        ratings = Rating.objects.filter(dish=dish)
        p = Paginator(ratings, 5)
        page = p.get_page(request.GET.get('page', 1))
        return render(request, 'users/dish.html', {
            'object': dish,
            'page_obj': page
        })


class SearchDishView(View):
    def get(self, request):
        query = self.request.GET.get('search')
        dishes = Dish.objects.filter(
            Q(dish_name__icontains=query) | Q(description__icontains=query),
            is_public=True
        )
        if dishes:
            p = Paginator(dishes, 10)
            page = p.get_page(request.GET.get('page', 1))
            return render(request, 'dishes.html', {
                'page_obj': page
            })
        else:
            return render(request, 'dishes.html', {
                'errors': NO_DISH_FOUND
            })
