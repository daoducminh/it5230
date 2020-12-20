from django.urls import path, include
from . import views, user_views, admin
import django_sb_admin.views

urlpatterns = [
    path('', views.index),
    path('login/<str:name>', user_views.LoginView.as_view()),

    path('admin/', include([
        path('', admin.Index.as_view(), name='admin_index'),
        path('login/', django_sb_admin.views.login, name='sb_admin_login'),
        path('user/', admin.UserManagement.as_view(), name='user_management'),
        path('dish/', admin.DishManagement.as_view(), name='dish_management'),
    ]))
]
