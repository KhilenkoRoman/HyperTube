from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
import requests
from a_player.models import FilmModel
import urllib
import json


# from urllib import parse

def api_request(query_term="0", limit=30, page=1, quality="All", genre="All", sort_by="rating", order_by="desc"):
    url = "https://yts.am/api/v2/list_movies.json"
    params = dict(
        query_term=query_term,
        limit=limit,
        page=page,
        quality=quality,
        genre=genre,
        sort_by=sort_by,
        order_by=order_by,
        with_rt_ratings=1,
    )
    resp = requests.get(url=url, params=params)
    print(resp)
    data = resp.json()
    print(data)
    print("++++++++++++++++++++++++++++++++")
    # save films in db
    if data['data']['movie_count'] > 0:
        if data['data']['movie_count'] > data['data']['limit']:
            counter = data['data']['limit']
        else:
            counter = data['data']['movie_count']
        print(counter)
        for i in range(counter):
            if len(FilmModel.objects.filter(imdb_id=data['data']['movies'][i]['imdb_code'])) == 0:
                FilmModel.objects.create(
                    name=data['data']['movies'][i]['title'],
                    imdb_id=data['data']['movies'][i]['imdb_code'], )

    return data


def search(request):
    context = {
        'APP_PATH': settings.APP_PATH,
        'data': api_request()
    }
    return render(request, 'search/search.html', context)


def filmSearch(request, film_name=""):
    context = {
        'APP_PATH': settings.APP_PATH,
        'data': api_request(film_name)
    }

    return render(request, 'search/search.html', context)


def ajax_search_request(request):
    data = api_request(request.POST.get('search_field'), 30, request.POST.get('page'), "All", request.POST.get('genre'),
                       request.POST.get('sort_by'))
    return JsonResponse(data, safe=False)
