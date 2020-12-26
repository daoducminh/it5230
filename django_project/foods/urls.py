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
                path('delete/', dish_views.DeleteDishView.as_view(), name='user_delete_dish'),
                # path('rate/', include([
                #     path('', dish_views.TestRating.as_view(), name='view_ratings')
                # path('add/', name='add_rating'),
                # path('update/', name='update_rating')
                # ]))
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
    path('dish/', dish_views.SearchDishView.as_view(), name='search_dish'),
    path('dish/<int:pk>/rate/', dish_views.AllRatingsView.as_view()),
    path('dish/<int:pk>/rate/add/', dish_views.CreateRatingView.as_view()),
    path('dish/<int:pk>/rate/update/', dish_views.UpdateRatingView.as_view()),
    path('dish/<int:pk>/update/', dish_views.UpdateDishView.as_view()),
    path('thanks/', views.thanks, name='thanks'),
    path('menu/', menu_views.index.as_view(), name="menu_index")
]
