from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Menu, Recipe
from .views import LoginRequiredView, SelfLoginView
from django.views.generic import View
from django.utils.decorators import method_decorator
import json
from .utilities.menu import convert_to_recipe_id


class DetailMenuView(View):
    def get(self, request, pk):
        menu = get_object_or_404(Menu, pk=pk)
        return render(request, 'test.html', {'menu': menu})


@method_decorator(csrf_exempt, name='dispatch')
class CreateMenuView(LoginRequiredView):
    def get(self, request):
        pass

    def post(self, request):
        menu = Menu()
        data = json.loads(request.body)
        menu.description = data['description']
        menu.user = request.user
        menu.save()
        ids = data['recipes']
        if not type(ids) is list:
            ids = convert_to_recipe_id(ids)
        recipes = Recipe.objects.filter(id__in=ids)
        menu.recipes.set(recipes)
        menu.save()
        return render(request, 'test.html')


class UpdateMenuView(SelfLoginView):
    def get(self, request, pk):
        pass

    def post(self, request, pk):
        pass


class DeleteMenuView(SelfLoginView):
    def get(self, request, pk):
        pass

    def post(self, request, pk):
        pass
