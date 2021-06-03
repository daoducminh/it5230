from django.shortcuts import render, redirect, get_object_or_404
from .models import Menu, Recipe
from django.views.generic import View
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Q


class SearchRecipeView(View):
    def get(self, request):
        recipe_name = self.request.GET.get('name')
        recipes = Recipe.objects.filter(
            Q(recipe_name__icontains=recipe_name)
        ).order_by('-review_number', '-score')[:5]
        data = [i for i in recipes.values()]
        return JsonResponse(data, safe=False)
