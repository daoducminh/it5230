from django.urls import path
from . import views, user_views

urlpatterns = [
    path('', views.index),
    path('login/<str:name>', user_views.LoginView.as_view())
]
