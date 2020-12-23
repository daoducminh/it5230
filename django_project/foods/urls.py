from django.urls import path, include
from . import views, user_views, admin_views

urlpatterns = [
    path('', views.index),
    path('accounts/profile/', user_views.ProfileView.as_view(), name='account_profile'),
    path('base/', admin_views.TestBase.as_view(), name='base'),
]
