from django.urls import path
from .views import index
urlpatterns = {
    path('', index.as_view(), name="menu_index")
}