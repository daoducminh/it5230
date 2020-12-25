from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
import re
import json
from foods.views import LoginRequiredView

# Create your views here.
class index(View):
    def get(self, request):
        return self.execute(request)
    def post(self, request):
        return self.execute(request)
    def execute(self, request, data={}):
        return render(request, 'menu/index.html')