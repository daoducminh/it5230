from functools import partial

from django.core import serializers
from django.http import JsonResponse
from django.views.generic import View

from .constants.recsys import get_model, get_data
# DATASET = get_data('dataset')
from .models import Recipe

TRAINSET = get_data('trainset')
SVD = get_model('svd')


def predict(algo, raw_uid, iid):
    r = algo.predict(raw_uid, iid)
    return r.iid, r.est


def get_top_n(raw_uid, trainset, algo):
    inner_uid = trainset.to_inner_uid(raw_uid)
    a1 = trainset.ur[inner_uid]
    rated_items = [i[0] for i in a1]
    all_items_set = set(trainset.all_items())
    rated_items_set = set(rated_items)
    need_items_set = all_items_set - rated_items_set

    fn = partial(predict, algo, inner_uid)
    preds = list(map(fn, list(need_items_set)))
    rs = sorted(preds, key=lambda x: x[1], reverse=True)
    return [trainset.to_raw_iid(i[0]) for i in rs[:10]]


class ItemSVDView(View):
    def get(self, request, pk):
        if request.user.is_authenticated and not request.user.is_staff:
            riid = get_top_n(request.user.pk, TRAINSET, SVD)
            recipes = Recipe.objects.filter(id__in=riid)
            data = serializers.serialize('json', recipes)
            return JsonResponse({'data': data})
        else:
            return JsonResponse({'data': {'a': 'User is not logged in.'}})
