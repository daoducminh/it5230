import django_sb_admin.views
from django.urls import path, include

from . import views, user_views, admin_views

urlpatterns = [
    path('', views.index),
    path('accounts/profile/', user_views.ProfileView.as_view(), name='account_profile'),
    path('test/', user_views.TestView.as_view()),

    path('admins/', include([
        path('', admin_views.HomeView.as_view(), name='admin_home'),
        path('login/', django_sb_admin.views.login, name='sb_admin_login'),
        path('user/', admin_views.UserManagementView.as_view(), name='user_management'),
        path('dish/', admin_views.DishManagementView.as_view(), name='dish_management'),
    ]))
]
