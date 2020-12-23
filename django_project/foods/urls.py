from django.urls import path, include
from . import views, user_views, admin_views
import django_sb_admin.views

urlpatterns = [
    path('', views.index),
    path('accounts/profile/', user_views.ProfileView.as_view(), name='account_profile'),
    path('admins/', include([
        path('login/', admin_views.Login.as_view(), name='admin_login'),
        path('logout/', admin_views.Logout.as_view(), name='admin_logout'),
        path('', admin_views.Index.as_view(), name='admin_index'),
        path('user/', admin_views.UserManagement.as_view(), name='user_management'),
        path('dish/', admin_views.DishManagement.as_view(), name='dish_management'),
    ])),
    path('base/', admin_views.TestBase.as_view(), name='base'),
]
