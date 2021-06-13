from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View


class LoginRequiredView(LoginRequiredMixin, View):
    login_url = '/accounts/login'


class SelfLoginView(UserPassesTestMixin, LoginRequiredView):
    def test_func(self):
        pass


class AdminOnlyView(SelfLoginView):
    def test_func(self):
        return self.request.user.is_staff
