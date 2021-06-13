from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth.models import User
from .models import Recipe, Menu
from django.core.paginator import Paginator
from .constants.pagination import *
from django.contrib import messages
from django.shortcuts import render
from .i18n.en import NO_RECIPE_FOUND, NO_MENU_FOUND, NO_PROFILE_FOUND


class MenuSearchRecipeView(View):
    def get(self, request):
        recipe_name = self.request.GET.get('name')
        recipes = Recipe.objects.filter(
            Q(recipe_name__icontains=recipe_name)
        ).order_by('-review_number', '-score')[:20]
        data = [i for i in recipes.values()]
        return JsonResponse(data, safe=False)


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
            menus = Menu.objects.filter(query).order_by('-review_number', '-score')[:240]
        else:
            menus = Menu.objects.all().order_by('-review_number', '-score')[:240]
        if menus:
            p = Paginator(menus, MENUS_PER_PAGE)
            page = p.get_page(request.GET.get('page', 1))
            return render(request, 'menu/list.html', {
                'page_obj': page
            })
        else:
            messages.error(request, NO_MENU_FOUND)
            return render(request, 'menu/list.html')


class SearchRecipeView(View):
    def get(self, request):
        query_name = request.GET.get('search')
        query_user = request.GET.get('user')
        if query_name or query_user:
            query = None
            if query_name:
                query = Q(recipe_name__icontains=query_name)
            if query_user:
                if query:
                    query = query | Q(user_id=query_user)
                else:
                    query = Q(user_id=query_user)
            recipes = Recipe.objects.filter(query).order_by('-review_number', '-score')[:240]
        else:
            recipes = Recipe.objects.all()[:240]
        if recipes:
            p = Paginator(recipes, RECIPES_PER_PAGE)
            page = p.get_page(request.GET.get('page', 1))
            return render(request, 'recipe/list.html', {
                'page_obj': page
            })
        else:
            messages.error(request, NO_RECIPE_FOUND)
            return render(request, 'recipe/list.html')


class SearchProfile(View):
    def get(self, request):
        query = self.request.GET.get('search')
        if query:
            users = User.objects.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query),
                is_active=True
            )
            if not users:
                users = User.objects.all().order_by('username')
                messages.error(request, NO_PROFILE_FOUND)
        else:
            users = User.objects.all().order_by('username')
        p = Paginator(users, PROFILES_PER_PAGE)
        page = p.get_page(request.GET.get('page', 1))
        return render(request, 'profiles.html', {
            'page_obj': page
        })
