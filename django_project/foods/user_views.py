from django.shortcuts import render

from .forms import UserForm
from .models import User
from .views import LoginRequiredView, UserUpdateView

# Testing purpose

class ProfileView(LoginRequiredView):
    def get(self, request):
        print(request.user.is_staff)
        user_info = request.user.user
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


class ProfileUpdate(UserUpdateView):
    # model = User
    # fields = ['height', 'weight', 'gender']
    form_class = UserForm
    queryset = User.objects.all()
    success_url = '/thanks/'
