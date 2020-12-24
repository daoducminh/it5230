from django.urls import path, include

from . import views, user_views, admin_views, dish_views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include([
        path('profile/', user_views.ProfileView.as_view(), name='account_profile'),
        path('register/', user_views.RegisterView.as_view(), name='account_register')
    ])),
    # path('accounts/', include([
    #
    # ])),
    path('admins/', include([
        path('login/', admin_views.Login.as_view(), name='admin_login'),
        path('logout/', admin_views.Logout.as_view(), name='admin_logout'),
        path('', admin_views.Index.as_view(), name='admin_index'),
        path('user/', admin_views.UserManagement.as_view(), name='user_management'),
        path('dish/', admin_views.DishManagement.as_view(), name='dish_management'),
    ])),
    path('profile/<int:pk>/', user_views.ProfileUpdate.as_view(), name='profile_update'),
    path('dish/<int:pk>/update/', dish_views.UpdateDishView.as_view()),
    path('thanks/', views.thanks, name='thanks')
]
