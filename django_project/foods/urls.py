from django.urls import path, include

from . import user_views, recipe_views, menu_views, search_views

urlpatterns = [
    path('', recipe_views.HomepageView.as_view(), name='index'),
    path('accounts/', include([
        path('register/', user_views.RegisterView.as_view(), name='register'),
        path('update/', user_views.UpdateProfileView.as_view(), name='update_profile')
    ])),
    path('recipe/', include([
        path('', search_views.SearchRecipeView.as_view(), name='search_recipe'),
        path('create/', recipe_views.CreateRecipeView.as_view(), name='recipe_create'),
        path('<int:pk>/', include([
            path('', recipe_views.RecipeDetailView.as_view(), name='recipe_detail'),
            path('rate/', recipe_views.UserRatingView.as_view(), name='rate_recipe'),
            path('update/', recipe_views.UpdateRecipeView.as_view(), name='recipe_update'),
            path('delete/', recipe_views.DeleteRecipeView.as_view(), name='self_delete_recipe')
        ])),
    ])),
    path('profile/', include([
        path('', search_views.SearchProfile.as_view(), name='search_profile'),
        path('<int:pk>/', include([
            path('', user_views.ProfileView.as_view(), name='profile_detail'),
            path('activate/', user_views.UpdateActivationView.as_view(), name='update_activation')
        ])),
    ])),
    path('category/<str:short_name>', recipe_views.CategoryView.as_view(), name='category'),
    path('menu/', include([
        path('', search_views.SearchMenuView.as_view(), name='search_menu'),
        path('<int:pk>/', include([
            path('', menu_views.DetailMenuView.as_view(), name='menu_detail'),
            path('rate/', menu_views.RateMenuView.as_view(), name='rate_menu'),
            path('update/', menu_views.UpdateMenuView.as_view(), name='menu_update'),
            path('delete/', menu_views.DeleteMenuView.as_view(), name='menu_delete')
        ])),
        path('create/', menu_views.CreateMenuView.as_view(), name='menu_create'),
    ])),
    path('search/', search_views.MenuSearchRecipeView.as_view(), name='menu_search_recipe'),
    # path('rec/recipe/<int:pk>/', recsys_views.ItemSVDView.as_view(), name='rec_recipe')
]
