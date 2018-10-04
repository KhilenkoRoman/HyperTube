from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
import requests
import urllib
import json


# from urllib import parse


def search(request):
    context = {'APP_PATH': settings.APP_PATH}
    return render(request, 'search/search.html', context)


def ajax_search_request(request):
    url = "https://yts.am/api/v2/list_movies.json"
    params = dict(
        query_term=request.POST.get('search_field'),
        limit=30,
        page=1,
        quality="All",
        genre="",
        sort_by="seeds"
    )

    resp = requests.get(url=url, params=params)
    data = resp.json()

    return JsonResponse(data, safe=False)
