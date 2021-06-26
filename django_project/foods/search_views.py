from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from .constants.pagination import *
from .i18n.en import NO_RECIPE_FOUND, NO_MENU_FOUND, NO_PROFILE_FOUND
from .models import Recipe, Menu


class MenuSearchRecipeView(View):
    def get(self, request):
        query_name = self.request.GET.get('name')
        if query_name:
            query = SearchQuery(query_name)
            recipes = Recipe.objects.annotate(rank=SearchRank(F('tsv'), query)).order_by('-rank')[:30]
            data = [i for i in recipes.values()]
            return JsonResponse(data, safe=False)


class SearchMenuView(View):
    def get(self, request):
        query_name = request.GET.get('search')
        query_user = request.GET.get('user')

        query_set = Menu.objects
        if query_name:
            query = SearchQuery(query_name)
            query_set = query_set.annotate(rank=SearchRank(F('tsv'), query))
            if query_user:
                query_set = query_set.filter(user_id=query_user)
            menus = query_set.order_by('-rank', '-review_number', '-score')[:240]
        else:
            if query_user:
                query_set = query_set.filter(user_id=query_user)
            else:
                query_set = query_set.all()
            menus = query_set.order_by('-review_number', '-score')[:240]

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

        query_set = Recipe.objects
        if query_name:
            query = SearchQuery(query_name)
            query_set = query_set.annotate(rank=SearchRank(F('tsv'), query))
            if query_user:
                query_set = query_set.filter(user_id=query_user)
            recipes = query_set.order_by('-rank', '-review_number', '-score')[:240]
        else:
            if query_user:
                query_set = query_set.filter(user_id=query_user)
            else:
                query_set = query_set.all()
            recipes = query_set.order_by('-review_number', '-score')[:240]

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
