from django.views.generic import View
from django.shortcuts import render

class index(View):
    def get(self, request):
        return self.execute(request)
    def post(self, request):
        return self.execute(request)
    def execute(self, request):
        return render(request, 'menu/index.html', None)

