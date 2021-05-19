from django.core import serializers
from django.http import JsonResponse
from django.views.generic import View

from .constants.recsys import get_model, get_data
# DATASET = get_data('dataset')
from .models import Dish

TRAINSET = get_data('trainset')
SVD = get_model('svd')


class KNNView(View):
    def get(self, request):
        pass


class SVDView(View):
    def get(self, request):
        pass


class ItemSVDView(View):
    def get(self, request, pk):
        iiid = TRAINSET.to_inner_iid(pk)
        # neighbors = SVD.predict(iiid)
        # riid = [TRAINSET.to_raw_iid(i) for i in neighbors]
        # rs = Dish.objects.filter(id__in=riid)
        # data = serializers.serialize('json', rs)
        return JsonResponse({'data': iiid})
