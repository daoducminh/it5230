from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View

from .constants.pagination import *
from .forms import RecipeForm, RatingForm
from .i18n.en import *
from .models import Recipe, Rating, Category
from .views import LoginRequiredView


@method_decorator(csrf_exempt, name='dispatch')
class UpdateRecipeView(LoginRequiredView):
    def post(self, request, pk):
        pass


@method_decorator(csrf_exempt, name='dispatch')
class DeleteRecipeView(LoginRequiredView):
    def post(self, request, pk):
        pass


class CreateRecipeView(LoginRequiredView):
    def get(self, request):
        return render(request, 'foods/recipe_add.html')

    def post(self, request):
        recipe_form = RecipeForm(request.POST, request.FILES)
        if recipe_form.is_valid():
            recipe = recipe_form.save(False)
            recipe.user = request.user
            recipe.save()
            messages.success(request, RECIPE_CREATED)
            if request.user.is_staff:
                return redirect('admin_all_recipes')
            else:
                return redirect('user_all_recipes')
        else:
            messages.error(request, recipe_form.errors)
            return render(request, 'foods/recipe_add.html')


class UserRatingView(LoginRequiredView):
    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if recipe.user != user:
            rating = Rating.objects.filter(recipe=recipe, user=user)
            if rating:
                rating_instance = rating.get()
                rating_form = RatingForm(request.POST, instance=rating_instance)
                if rating_form.is_valid():
                    rating_form.save()
                    messages.success(request, RATE_UPDATED)
                else:
                    messages.error(request, rating_form.errors)
            else:
                rating_form = RatingForm(request.POST)
                if rating_form.is_valid():
                    rating = rating_form.save(False)
                    rating.recipe = recipe
                    rating.user = user
                    rating.save()
                    messages.success(request, RATE_CREATED)
                else:
                    messages.error(request, rating_form.errors)
        return redirect('recipe_detail', pk=pk)


class RecipeDetailView(View):
    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        s = round(recipe.score)
        ratings = Rating.objects.filter(recipe=recipe).order_by('-updated_at')
        p = Paginator(ratings, RATINGS_PER_PAGE)
        page = p.get_page(request.GET.get('page', 1))
        context = {
            'recipe': recipe,
            'page_obj': page,
            'score': s
        }
        user = request.user
        if user.is_authenticated and user.pk != recipe.user.pk:
            user_rating = Rating.objects.filter(recipe=recipe, user=user)
            if user_rating:
                context['user_rating'] = user_rating.get()
        return render(request, 'recipes/detail.html', context)


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
            return render(request, 'recipes/list.html', {
                'page_obj': page
            })
        else:
            messages.error(request, NO_RECIPE_FOUND)
            return render(request, 'recipes/list.html')


class HomepageView(View):
    def get(self, request):
        veg = Recipe.objects.filter(
            Q(category_id=4) &
            Q(image_url__isnull=False),
        ).order_by('-review_number', '-score')[:5]
        return render(request, 'index.html', {
            'veg': veg
        })


class CategoryView(View):
    def get(self, request, short_name):
        category = get_object_or_404(Category, short_name=short_name)
        recipes = Recipe.objects.filter(category=category).order_by('-review_number', '-score')[:60]
        if recipes:
            p = Paginator(recipes, RECIPES_PER_PAGE)
            page = p.get_page(request.GET.get('page', 1))
            return render(request, 'recipes/list.html', {
                'page_obj': page
            })
        else:
            messages.error(request, NO_RECIPE_FOUND)
            return render(request, 'recipes/list.html')
