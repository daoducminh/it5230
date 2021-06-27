from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from .constants.pagination import *
from .constants.recipe import *
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
        params = request.GET.dict()
        q_search = params.get('search')
        q_user = params.get('user')
        q_min = params.get('min')
        q_max = params.get('max')
        q_sort = params.get('sort')
        current_page = params.get('page')
        filter_query = None
        order = None

        query_set = Recipe.objects
        # Handle parameter for full-text search
        if q_search:
            ts_query = SearchQuery(q_search)
            query_set = query_set.annotate(rank=SearchRank(F('tsv'), ts_query))
        # Handle parameter for user id
        if q_user:
            filter_query = Q(user_id=q_user)
        # Handle parameter for calories range
        if q_min or q_max:
            try:
                q_min = int(q_min)
            except TypeError:
                q_min = MIN_CALORIES
            try:
                q_max = int(q_max)
            except TypeError:
                q_max = MAX_CALORIES
            if filter_query:
                filter_query = filter_query | Q(calories__range=(q_min, q_max))
            else:
                filter_query = Q(calories__range=(q_min, q_max))
        # Combine all needed filters
        if filter_query:
            query_set = query_set.filter(filter_query)
        else:
            query_set = query_set.all()
        # Handle recipes' order
        if q_sort:
            if q_sort == 'latest':
                order = ('-updated_at',)
            else:
                order = ('-review_number', '-score')
        # Handle pagination
        try:
            current_page = int(current_page)
        except TypeError:
            current_page = 1
        index = (current_page - 1) * RECIPES_PER_PAGE
        # Make query
        recipes = query_set.order_by(*order)[index:index + RECIPES_PER_PAGE]

        if recipes:
            next_index = current_page * RECIPES_PER_PAGE
            next_recipes = query_set.order_by(*order)[next_index:next_index + RECIPES_PER_PAGE]
            page_obj = {'current_page': current_page}
            if next_recipes:
                page_obj['next_page'] = current_page + 1
            if current_page > 1:
                page_obj['prev_page'] = current_page - 1

            return render(request, 'recipe/list.html', {
                'recipes': recipes,
                'page_obj': page_obj,
                'search': True
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
