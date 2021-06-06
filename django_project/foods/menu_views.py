from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .constants.pagination import RATINGS_PER_PAGE, MENUS_PER_PAGE
from .models import Menu, Recipe, MenuRating
from django.db.models import Q
from .views import LoginRequiredView
from django.views.generic import View
from django.utils.decorators import method_decorator
import json
from .utilities.menu import convert_to_recipe_id
from django.http import JsonResponse
from .i18n.en import MENU_CREATED, MENU_UPDATED, MENU_DELETED, NO_MENU_FOUND, NOT_ALLOWED, INVALID_DATA, RATE_UPDATED, \
    RATE_CREATED, TITLE_CREATE_MENU, TITLE_UPDATE_MENU
from .forms import MenuRatingForm


class SearchMenuView(View):
    def get(self, request):
        query_name = request.GET.get('search')
        query_user = request.GET.get('user')

        if query_name or query_user:
            query = None
            if query_name:
                query = Q(menu_name__icontains=query_name)
            if query_user:
                if query:
                    query = query | Q(user_id=query_user)
                else:
                    query = Q(user_id=query_user)
            menus = Menu.objects.filter(query)[:24]
        else:
            menus = Menu.objects.all()[:24]
        if menus:
            p = Paginator(menus, MENUS_PER_PAGE)
            page = p.get_page(request.GET.get('page', 1))
            return render(request, 'menus/list.html', {
                'page_obj': page
            })
        else:
            messages.error(request, NO_MENU_FOUND)
            return render(request, 'menus/list.html')


class DetailMenuView(View):
    def get(self, request, pk):
        menu = get_object_or_404(Menu, pk=pk)
        ratings = MenuRating.objects.filter(menu=menu)
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

        return render(request, 'menus/detail.html', {
            'menu': menu,
            'recipes': recipes,
            'total_calories': total_calories,
            'hours': total_time // 60,
            'minutes': total_time % 60,
            'page_obj': page
        })


@method_decorator(csrf_exempt, name='dispatch')
class CreateMenuView(LoginRequiredView):
    def get(self, request):
        return render(request, 'menus/edit.html', {'title': TITLE_CREATE_MENU})

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
        return render(request, 'menus/edit.html', {
            'menu': menu,
            'recipes': recipes,
            'title': TITLE_UPDATE_MENU
        })

    def post(self, request, pk):
        menu = get_object_or_404(Menu, pk=pk)
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


@method_decorator(csrf_exempt, name='dispatch')
class DeleteMenuView(LoginRequiredView):
    def post(self, request, pk):
        menu = get_object_or_404(Menu, pk=pk)
        if menu.user.pk == request.user.pk or request.user.is_staff:
            menu.delete()
            return JsonResponse({'message': MENU_DELETED})
        else:
            return JsonResponse({'message': NOT_ALLOWED}, status=500)


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
