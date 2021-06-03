from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Menu, Recipe, MenuRating
from .views import LoginRequiredView, SelfLoginView
from django.views.generic import View
from django.utils.decorators import method_decorator
import json
from .utilities.menu import convert_to_recipe_id
from django.http import JsonResponse
from .i18n.en import MENU_CREATED, MENU_UPDATED, MENU_DELETED, NO_MENU_FOUND, NOT_ALLOWED, INVALID_DATA, RATE_UPDATED, \
    RATE_CREATED
from .forms import MenuRatingForm


class DetailMenuView(View):
    def get(self, request, pk):
        menu = get_object_or_404(Menu, pk=pk)
        return render(request, 'menus/detail.html', {'menu': menu})


@method_decorator(csrf_exempt, name='dispatch')
class CreateMenuView(LoginRequiredView):
    def get(self, request):
        return render(request, 'menus/edit.html')

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
        return render(request, 'menus/edit.html', {'menu': menu})

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
