from django.urls import path, include
from . import views, user_views, admin
import django_sb_admin.views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index),
    path('login/<str:name>', user_views.LoginView.as_view()),

    path('admin/', include([
        path('', django_sb_admin.views.start, name='sb_admin_start'),
        path('register/', TemplateView.as_view(
            template_name="django_sb_admin/register.html"),
            name='sb_admin_register'
        ),
        path('forgot_password/', TemplateView.as_view(
            template_name="django_sb_admin/forgot_password.html"),
            name='sb_admin_forgot_password'
        ),
        path('404/', TemplateView.as_view(
            template_name="django_sb_admin/sb_admin_404.html"),
            name='sb_admin_404'
        ),
        path('login/', django_sb_admin.views.login, name='sb_admin_login'),
        path('dashboard/', admin.Login.as_view(), name='sb_admin_dashboard'),
        path('charts/', django_sb_admin.views.charts, name='sb_admin_charts'),
        path('tables/', django_sb_admin.views.tables, name='sb_admin_tables'),
        path('forms/', django_sb_admin.views.forms, name='sb_admin_forms'),
        path('bootstrap-elements/', django_sb_admin.views.bootstrap_elements,
            name='sb_admin_bootstrap_elements'),
        path('bootstrap-grid/', django_sb_admin.views.bootstrap_grid,
            name='sb_admin_bootstrap_grid'),
        path('rtl-dashboard/', django_sb_admin.views.rtl_dashboard,
            name='sb_admin_rtl_dashboard'),
        path('blank/', django_sb_admin.views.blank, name='sb_admin_blank'),
    ]))
]
