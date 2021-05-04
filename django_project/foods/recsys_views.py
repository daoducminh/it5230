from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import View
from django.http import JsonResponse
from .constants.pagination import *
from django.core import serializers
from .i18n.en import *
from .models import Dish, Rating
from .views import SelfUpdateView, SelfDeleteView, UserListView, LoginRequiredView, UserOnlyView, AdminOnlyView, \
    AdminListView, SuperuserDeleteView
from .constants.recsys import get_model, get_data

DATASET = get_data('dataset')
TRAINSET = get_data('trainsetfull')
KNN = get_model('knn_m')
SVD = get_model('svd')


class KNNView(View):
    def get(self, request):
        pass


class SVDView(View):
    def get(self, request):
        pass


class ItemKNNView(View):
    def get(self, request, pk):
        iiid = TRAINSET.to_inner_iid(str(pk))
        neighbors = KNN.get_neighbors(iid=iiid, k=10)
        riid = [TRAINSET.to_raw_iid(i) for i in neighbors]
        rs = Dish.objects.filter(id__in=riid)
        data = serializers.serialize('json', rs)
        return JsonResponse({'data': data})
