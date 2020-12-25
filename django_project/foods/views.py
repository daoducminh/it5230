from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView


def index(request):
    context = {
        'app_name': 'Foods'
    }
    return render(request, 'index.html', context)


class LoginRequiredView(LoginRequiredMixin, View):
    login_url = '/accounts/login'


class SelfLoginView(UserPassesTestMixin, LoginRequiredView):
    def test_func(self):
        pass


class UserDetailView(DetailView, SelfLoginView):
    def test_func(self):
        return (not self.request.user.is_staff) and (self.request.user.pk == self.get_object().user.pk)


class UserListView(ListView, SelfLoginView):
    def test_func(self):
        return not self.request.user.is_staff


class UserCreateView(CreateView, SelfLoginView):
    def test_func(self):
        return (not self.request.user.is_staff) and (self.request.user.pk == self.get_object().user.pk)


class UserUpdateView(UpdateView, SelfLoginView):
    def test_func(self):
        return (not self.request.user.is_staff) and (self.request.user.pk == self.get_object().user.pk)


class UserDeleteView(DeleteView, SelfLoginView):
    def test_func(self):
        return (not self.request.user.is_staff) and (self.request.user.pk == self.get_object().user.pk)


class AdminDetailView(DetailView, SelfLoginView):
    def test_func(self):
        return self.request.user.is_staff and (self.request.user.pk == self.get_object().user.pk)


class AdminListView(ListView, SelfLoginView):
    def test_func(self):
        return self.request.user.is_staff


class AdminCreateView(CreateView, SelfLoginView):
    def test_func(self):
        return self.request.user.is_staff and (self.request.user.pk == self.get_object().user.pk)


class AdminUpdateView(UpdateView, SelfLoginView):
    def test_func(self):
        return self.request.user.is_staff and (self.request.user.pk == self.get_object().user.pk)


class AdminDeleteView(DeleteView, SelfLoginView):
    def test_func(self):
        return self.request.user.is_staff and (self.request.user.pk == self.get_object().user.pk)


class SelfCreateView(CreateView, SelfLoginView):
    def test_func(self):
        return self.request.user.pk == self.get_object().user.pk


class SelfUpdateView(UpdateView, SelfLoginView):
    def test_func(self):
        return self.request.user.pk == self.get_object().user.pk


class SelfDeleteView(DeleteView, SelfLoginView):
    def test_func(self):
        return self.request.user.pk == self.get_object().user.pk


def thanks(request):
    return render(request, 'thanks.html')
