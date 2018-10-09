from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
import requests
from a_player.models import FilmModel
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
        page=request.POST.get('page'),
        quality="All",
        genre="",
        sort_by="seeds"
    )

    resp = requests.get(url=url, params=params)

    data = resp.json()

    # save films in db
    if data['data']['movie_count'] > 0:
        if data['data']['movie_count'] > data['data']['limit']:
            counter = data['data']['limit']
        else:
            counter = data['data']['movie_count']
        for i in range(counter):
            if len(FilmModel.objects.filter(imdb_id=data['data']['movies'][i]['imdb_code'])) == 0:
                FilmModel.objects.create(
                    name=data['data']['movies'][i]['title'],
                    imdb_id=data['data']['movies'][i]['imdb_code'], )

    return JsonResponse(data, safe=False)
