from django.urls import path, include

from . import user_views, recipe_views, menu_views

urlpatterns = [
    path('', recipe_views.AllPublicRecipeView.as_view(), name='index'),
    path('accounts/', include([
        path('register/', user_views.RegisterView.as_view(), name='register'),
    ])),
    path('users/', include([
        path('profile/', user_views.UpdateProfileView.as_view(), name='account_profile'),
        path('recipe/', include([
            path('', recipe_views.UserAllRecipeView.as_view(), name='user_all_recipes'),
            path('add/', recipe_views.CreateRecipeView.as_view(), name='user_add_recipe'),
            path('<int:pk>/', include([
                path('', recipe_views.UserRecipeView.as_view(), name='user_recipe_detail'),
                path('update/', recipe_views.UpdateRecipeView.as_view(), name='user_update_recipe'),
                path('delete/', recipe_views.DeleteRecipeView.as_view(), name='user_delete_recipe')
            ]))
        ]))
    ])),
    path('admins/', include([
        # path('', admin_views.Index.as_view(), name='admin_index'),
        # path('user/', admin_views.UserManagement.as_view(), name='user_management'),
        path('profile/', user_views.AdminSearchProfile.as_view(), name='admin_search_profile'),
        path('recipe/', include([
            path('', recipe_views.AdminAllRecipeView.as_view(), name='admin_all_recipes'),
            path('add/', recipe_views.CreateRecipeView.as_view(), name='admin_add_recipe'),
            path('<int:pk>/', include([
                path('', recipe_views.AdminRecipeView.as_view(), name='admin_recipe_detail'),
                path('update/', recipe_views.UpdateRecipeView.as_view(), name='admin_update_recipe'),
                path('delete/', recipe_views.DeleteRecipeView.as_view(), name='admin_delete_recipe')
            ]))
        ])),
    ])),
    path('recipe/', include([
        path('', recipe_views.SearchRecipeView.as_view(), name='search_recipe'),
        path('<int:pk>/', include([
            path('', recipe_views.RecipeDetailView.as_view(), name='recipe_detail'),
            path('rate/', recipe_views.UserRatingView.as_view(), name='user_rating'),
            path('delete/', recipe_views.SuperuserDeleteRecipeView.as_view(), name='self_delete_recipe')
        ])),
    ])),
    path('profile/', include([
        path('', user_views.SearchProfile.as_view(), name='search_profile'),
        path('<int:pk>/', include([
            path('', user_views.ProfileView.as_view(), name='profile_detail'),
            path('activate/', user_views.UpdateActivationView.as_view(), name='update_activation')
        ])),
    ])),
    path('category/<str:short_name>', recipe_views.CategoryView.as_view(), name='category'),
    path('menu/', include([
        path('create/', menu_views.CreateMenuView.as_view(), name='menu_create'),
    ])),
    # path('menu/', include([
    #     path('', menu_views.index.as_view(), name="menu_index"),
    #     path('create', menu_views.create.as_view(), name="menu_create"),
    #     path('create_query', menu_views.create_query.as_view(), name="menu_create_query"),
    #     path('update_query', menu_views.update_query.as_view(), name="menu_update_query"),
    #     path('clone_query', menu_views.clone_query.as_view(), name="menu_clone_query"),
    #     path('delete_query', menu_views.delete_query.as_view(), name="menu_delete_query"),
    #     path('history', menu_views.history.as_view(), name="menu_history"),
    #     path('detail/<int:menu_id>', menu_views.detail.as_view(), name="menu_detail"),
    #     path('update', menu_views.update.as_view(), name="menu_update"),
    #     path('delete', menu_views.delete.as_view(), name="menu_delete"),
    #     path('query_filter_recipe', menu_views.query_filter_recipe, name="menu_query_filter_recipe")
    # ])),
    # path('rec/recipe/<int:pk>/', recsys_views.ItemSVDView.as_view(), name='rec_recipe')
]

handler404 = 'foods.views.error_404'
handler500 = 'foods.views.error_500'
