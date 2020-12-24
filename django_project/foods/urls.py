from django.urls import path, include
from . import views, user_views, admin_views, dish_views

urlpatterns = [
    path('', views.index),
    path('accounts/profile/', user_views.ProfileView.as_view(), name='account_profile'),
    path('base/', admin_views.TestBase.as_view(), name='base'),
    path('dishes/', dish_views.AllDishView.as_view(), name='all_dish_view'),
    path('dishes/<int:dish_id>/', dish_views.DishView.as_view(), name='dish_view'),
]
