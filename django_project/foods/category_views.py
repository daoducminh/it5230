from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from .constants.pagination import CATEGORIES_PER_PAGE, RECIPES_PER_PAGE
from .forms import CategoryForm
from .i18n.en import *
from .models import Recipe, Category
from .utilities.category import convert_category_title
from .views import AdminOnlyView


class RecipesByCategoryView(View):
    def get(self, request, short_name):
        category = get_object_or_404(Category, short_name=short_name)
        current_page = request.GET.get('page')
        try:
            current_page = int(current_page)
        except TypeError:
            current_page = 1
        index = (current_page - 1) * RECIPES_PER_PAGE
        query_set = Recipe.objects.filter(category=category).order_by('-review_number', '-score')
        recipes = query_set[index:index + RECIPES_PER_PAGE]
        if recipes:
            next_index = current_page * RECIPES_PER_PAGE
            next_recipes = query_set[next_index:next_index + RECIPES_PER_PAGE]
            page_obj = {'current_page': current_page}

            if next_recipes:
                page_obj['next_page'] = current_page + 1
            if current_page > 1:
                page_obj['prev_page'] = current_page - 1

            return render(request, 'recipe/list.html', {
                'recipes': recipes,
                'page_obj': page_obj
            })
        else:
            messages.error(request, NO_RECIPE_FOUND)
            return render(request, 'recipe/list.html')


class CreateCategoryView(AdminOnlyView):
    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            c = form.save(False)
            c.short_name = convert_category_title(c.title)
            c.save()
            messages.success(request, CATEGORY_CREATED)
        else:
            messages.error(request, form.errors)
        return redirect('search_category')


class UpdateCategoryView(AdminOnlyView):
    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, CATEGORY_UPDATED)
        else:
            messages.error(request, form.errors)
        return redirect('search_category')


class ListCategoryView(View):
    def get(self, request):
        current_page = request.GET.get('page')
        try:
            current_page = int(current_page)
        except TypeError:
            current_page = 1
        index = (current_page - 1) * CATEGORIES_PER_PAGE
        categories = Category.objects.all()[index:index + CATEGORIES_PER_PAGE]
        if categories:
            categories = tuple(c for c in categories.values())
            for c in categories:
                count = Recipe.objects.filter(category_id=c['id']).count()
                c['count'] = count
            next_index = current_page * CATEGORIES_PER_PAGE
            next_categories = Category.objects.all()[next_index:next_index + CATEGORIES_PER_PAGE]
            page_obj = {'current_page': current_page}
            if next_categories:
                page_obj['next_page'] = current_page + 1
            if current_page > 1:
                page_obj['prev_page'] = current_page - 1
            return render(request, 'category/list.html', {
                'categories': categories,
                'page_obj': page_obj
            })
