from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import re
import json


# Create your views here.
def menu_index(request):
    return HttpResponse("Menu Index")
