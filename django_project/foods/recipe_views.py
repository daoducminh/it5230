from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import View

from .constants.pagination import *
from .forms import RecipeForm, RatingForm
from .i18n.en import *
from .models import Recipe, Rating, Category
from .views import SelfUpdateView, SelfDeleteView, UserListView, LoginRequiredView, UserOnlyView, AdminOnlyView, \
    AdminListView, SuperuserDeleteView


class AdminRecipeView(AdminOnlyView):
    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        ratings = Rating.objects.filter(recipe=recipe)
        p = Paginator(ratings, RATINGS_PER_PAGE)
        page = p.get_page(request.GET.get('page', 1))
        return render(request, 'admins/recipe.html', {
            'object': recipe,
            'page_obj': page
        })


class AdminAllRecipeView(AdminListView):
    model = Recipe
    template_name = 'admins/recipes.html'
    queryset = Recipe.objects.all()
    paginate_by = RECIPES_PER_PAGE

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_context_data(self, **kwarg):
        context = super().get_context_data(**kwarg)
        return context


class UserRecipeView(UserOnlyView):
    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        ratings = Rating.objects.filter(recipe=recipe)
        p = Paginator(ratings, RATINGS_PER_PAGE)
        page = p.get_page(request.GET.get('page', 1))
        return render(request, 'users/recipe.html', {
            'object': recipe,
            'page_obj': page
        })


class UserAllRecipeView(UserListView):
    model = Recipe
    template_name = 'users/recipes.html'
    queryset = Recipe.objects.all()
    paginate_by = RECIPES_PER_PAGE

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_context_data(self, **kwarg):
        context = super().get_context_data(**kwarg)
        return context


class UpdateRecipeView(SelfUpdateView):
    form_class = RecipeForm
    queryset = Recipe.objects.all()
    success_message = RECIPE_UPDATED

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse('admin_recipe_detail', kwargs={'pk': self.object.pk})
        else:
            return reverse('user_recipe_detail', kwargs={'pk': self.object.pk})


class DeleteRecipeView(SelfDeleteView):
    model = Recipe
    success_message = RECIPE_DELETED

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse('admin_all_recipes')
        else:
            return reverse('user_all_recipes')


class SuperuserDeleteRecipeView(SuperuserDeleteView):
    model = Recipe
    success_message = RECIPE_DELETED

    def get_success_url(self):
        return reverse('index')


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


class UserRatingView(UserOnlyView):
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
            'object': recipe,
            'page_obj': page,
            'score': s
        }
        user = request.user
        if user.is_authenticated and not user.is_staff:
            user_rating = Rating.objects.filter(recipe=recipe, user=user)
            if user_rating:
                context['user_rating'] = user_rating.get()
        return render(request, 'recipe.html', context)


class SearchRecipeView(View):
    def get(self, request):
        query = self.request.GET.get('search')
        recipes = Recipe.objects.filter(
            Q(recipe_name__icontains=query) |
            Q(description__icontains=query) |
            Q(ingredients__icontains=query)
        ).order_by('-review_number', '-score')[:24]
        if not recipes:
            recipes = Recipe.objects.all()[:24]
            messages.error(request, NO_RECIPE_FOUND)
        p = Paginator(recipes, RECIPES_PER_PAGE)
        page = p.get_page(request.GET.get('page', 1))
        return render(request, 'recipes.html', {
            'page_obj': page
        })


class AllPublicRecipeView(View):
    def get(self, request):
        veg = Recipe.objects.filter(
            Q(category_id=4) &
            Q(image_url__isnull=False),
        ).order_by('-review_number', '-score')[:5]
        # if recipes:
        #     p = Paginator(recipes, RECIPES_PER_PAGE)
        #     page = p.get_page(request.GET.get('page', 1))
        #     return render(request, 'recipes.html', {
        #         'page_obj': page
        #     })
        # else:
        #     messages.error(request, NO_RECIPE_FOUND)
        #     return render(request, 'recipes.html')
        # return render(request, 'recipes.html', {
        #     'recipe': recipes
        # })
        data = [i for i in veg.values()]
        return render(request, 'index.html', {
            'veg': data
        })


class CategoryView(View):
    def get(self, request, short_name):
        category = get_object_or_404(Category, short_name=short_name)
        recipes = Recipe.objects.filter(category=category).order_by('-review_number', '-score')[:60]
        if recipes:
            p = Paginator(recipes, RECIPES_PER_PAGE)
            page = p.get_page(request.GET.get('page', 1))
            return render(request, 'recipes.html', {
                'page_obj': page
            })
        else:
            messages.error(request, NO_RECIPE_FOUND)
            return render(request, 'recipes.html')
