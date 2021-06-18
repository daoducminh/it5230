import json

from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from .constants.pagination import RATINGS_PER_PAGE
from .forms import MenuRatingForm
from .i18n.en import *
from .models import Menu, Recipe, MenuRating
from .utilities.menu import convert_to_recipe_id
from .views import LoginRequiredView


class DetailMenuView(View):
    def get(self, request, pk):
        menu = get_object_or_404(Menu, pk=pk)
        ratings = MenuRating.objects.filter(menu=menu).order_by('-updated_at')
        p = Paginator(ratings, RATINGS_PER_PAGE)
        page = p.get_page(request.GET.get('page', 1))
        recipes = menu.recipes.all()
        total_calories = 0
        total_time = 0
        menu.round_score = round(menu.score)
        for r in recipes:
            r.round_score = round(r.score)
            total_time += r.total_time
            total_calories += r.calories
        context = {
            'menu': menu,
            'recipes': recipes,
            'total_calories': total_calories,
            'hours': total_time // 60,
            'minutes': total_time % 60,
            'page_obj': page
        }
        user = request.user
        if user.is_authenticated and user.pk != menu.user.pk:
            user_rating = MenuRating.objects.filter(menu=menu, user=user)
            if user_rating:
                context['user_rating'] = user_rating.get()

        return render(request, 'menu/detail.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class CreateMenuView(LoginRequiredView):
    def get(self, request):
        return render(request, 'menu/edit.html', {'title': TITLE_CREATE_MENU})

    def post(self, request):
        data = json.loads(request.body)
        if data:
            menu = Menu()
            menu.menu_name = data['menuName']
            menu.description = data['description']
            menu.user = request.user
            menu.save(False)
            ids = data['recipes']
            if not type(ids) is list:
                ids = convert_to_recipe_id(ids)
            recipes = Recipe.objects.filter(id__in=ids)
            menu.recipes.set(recipes)
            menu.save()
            return JsonResponse({'message': MENU_CREATED})
        else:
            return JsonResponse({'message': INVALID_DATA}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateMenuView(LoginRequiredView):
    def get(self, request, pk):
        menu = get_object_or_404(Menu, pk=pk)
        recipes = menu.recipes.all()
        for r in recipes:
            r.round_score = round(r.score)
        return render(request, 'menu/edit.html', {
            'menu': menu,
            'recipes': recipes,
            'title': TITLE_UPDATE_MENU
        })

    def post(self, request, pk):
        try:
            menu = Menu.objects.get(pk=pk)
            data = json.loads(request.body)
            if data:
                if menu.user.pk == request.user.pk or request.user.is_staff:
                    menu.menu_name = data['menuName']
                    menu.description = data['description']
                    ids = data['recipes']
                    if not type(ids) is list:
                        ids = convert_to_recipe_id(ids)
                    recipes = Recipe.objects.filter(id__in=ids)
                    menu.recipes.set(recipes)
                    menu.save()
                    return JsonResponse({'message': MENU_UPDATED})
                else:
                    return JsonResponse({'message': NOT_ALLOWED}, status=500)
            else:
                return JsonResponse({'message': INVALID_DATA}, status=500)
        except:
            return JsonResponse({'message': NO_MENU_FOUND})


@method_decorator(csrf_exempt, name='dispatch')
class DeleteMenuView(LoginRequiredView):
    def post(self, request, pk):
        try:
            menu = Menu.objects.get(pk=pk)
            if menu.user.pk == request.user.pk or request.user.is_staff:
                menu.delete()
                return JsonResponse({'message': MENU_DELETED})
            else:
                return JsonResponse({'message': NOT_ALLOWED}, status=500)
        except:
            return JsonResponse({'message': NO_MENU_FOUND}, status=500)


class RateMenuView(LoginRequiredView):
    def post(self, request, pk):
        menu = get_object_or_404(Menu, pk=pk)
        user = request.user
        if menu.user != user:
            rating = MenuRating.objects.filter(menu=menu, user=user)
            if rating:
                rating_instance = rating.get()
                rating_form = MenuRatingForm(request.POST, instance=rating_instance)
                if rating_form.is_valid():
                    rating_form.save()
                    messages.success(request, RATE_UPDATED)
                else:
                    messages.error(request, rating_form.errors)
            else:
                rating_form = MenuRatingForm(request.POST)
                if rating_form.is_valid():
                    rating = rating_form.save(False)
                    rating.user = user
                    rating.menu = menu
                    rating.save()
                    messages.success(request, RATE_CREATED)
                else:
                    messages.error(request, rating_form.errors)
        return redirect('menu_detail', pk=pk)
