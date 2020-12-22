from django.contrib.auth.models import User
from django.shortcuts import render

from .views import UserRequiredView


class ProfileView(UserRequiredView):
    def get(self, request):
        user = User.objects.get(username=request.user.username)
        user_info = user.user
        context = {
            'height': user_info.height,
            'weight': user_info.weight,
            'gender': user_info.gender
        }
        return render(request, 'registration/profile.html', context)

    def post(self, request):
        height = request.POST['height']
        weight = request.POST['weight']
        gender = request.POST['gender']
        gender = True if gender == 'male' else False
        user_info = request.user.user
        user_info.height = height
        user_info.weight = weight
        user_info.gender = gender
        user_info.save()
        context = {
            'height': height,
            'weight': weight,
            'gender': gender,
            'message': 'Updated successfully'
        }
        return render(request, 'registration/profile.html', context)
