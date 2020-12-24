from django.urls import path, include

from . import views, user_views, admin_views, dish_views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include([
        path('profile/', user_views.ProfileView.as_view(), name='account_profile'),
        path('register/', user_views.RegisterView.as_view(), name='account_register'),
        path('dish/', include([
            # path('',,name='user_all_dishes'),
            path('<int:pk>/', include([
                # path('',,name='user_dish_detail'),
                path('update/', dish_views.UserUpdateDishView.as_view(), name='user_update_dish'),
                path('delete/', dish_views.UserDeleteDishView.as_view(), name='user_delete_dish')
            ]))
        ]))
    ])),
    path('admins/', include([
        path('login/', admin_views.Login.as_view(), name='admin_login'),
        path('logout/', admin_views.Logout.as_view(), name='admin_logout'),
        path('', admin_views.Index.as_view(), name='admin_index'),
        path('user/', admin_views.UserManagement.as_view(), name='user_management'),
        path('dish/', include([
            path('', dish_views.AdminAllDishView.as_view(), name='dish_management'),
            path('<int:pk>/', include([
                path('', dish_views.AdminDishView.as_view(), name='user_dish_detail'),
                path('update/', dish_views.UserUpdateDishView.as_view(), name='admin_update_dish'),
                path('delete/', dish_views.UserDeleteDishView.as_view(), name='admin_delete_dish')
            ]))
        ])),
    ])),
    path('thanks/', views.thanks, name='thanks'),

    # test view
    path('base/', admin_views.TestBase.as_view(), name='base'),
]
