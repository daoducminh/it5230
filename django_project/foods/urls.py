from django.urls import path, include

from . import views, user_views, dish_views, menu_views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include([
        path('register/', user_views.RegisterView.as_view(), name='register'),

    ])),
    path('users/', include([
        path('profile/', user_views.UpdateProfileView.as_view(), name='account_profile'),
        path('dish/', include([
            path('', dish_views.UserAllDishView.as_view(), name='user_all_dishes'),
            path('add/', dish_views.CreateDishView.as_view(), name='user_add_dish'),
            path('<int:pk>/', include([
                path('', dish_views.UserDishView.as_view(), name='user_dish_detail'),
                path('update/', dish_views.UpdateDishView.as_view(), name='user_update_dish'),
                path('delete/', dish_views.DeleteDishView.as_view(), name='user_delete_dish')
            ]))
        ]))
    ])),
    path('admins/', include([
        # path('', admin_views.Index.as_view(), name='admin_index'),
        # path('user/', admin_views.UserManagement.as_view(), name='user_management'),
        path('dish/', include([
            path('', dish_views.AdminAllDishView.as_view(), name='admin_all_dishes'),
            path('add/', dish_views.CreateDishView.as_view(), name='admin_add_dish'),
            path('<int:pk>/', include([
                path('', dish_views.AdminDishView.as_view(), name='admin_dish_detail'),
                path('update/', dish_views.UpdateDishView.as_view(), name='admin_update_dish'),
                path('delete/', dish_views.DeleteDishView.as_view(), name='admin_delete_dish')
            ]))
        ])),
    ])),
    path('dish/', include([
        path('', dish_views.SearchDishView.as_view(), name='search_dish'),
        path('<int:pk>/', include([
            path('', dish_views.DishDetailView.as_view(), name='dish_detail'),
            path('rate/', dish_views.UserRatingView.as_view(), name='user_rating'),
        ])),

    ])),
    path('menu/', menu_views.index.as_view(), name="menu_index")
]
