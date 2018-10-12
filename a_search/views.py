from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, HttpResponse
import requests
from a_player.models import FilmModel, CommentModel


def api_request(query_term="", limit=30, page=1, quality="All", genre="", sort_by="rating", order_by="desc"):
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

    try:
        data = resp.json()
    except:
        return 0
    movie_count = len(data['data']['movies'])
    if movie_count > 0:
        for i in range(movie_count):
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
        'data': api_request(film_name, 30, request.GET.get('page'), "All", request.GET.get('genre'), request.GET.get('sort_by'))
    }
    return render(request, 'search/search.html', context)


def ajax_search_request(request):
    data = api_request(request.POST.get('search_field'), 30, request.POST.get('page'), "All", request.POST.get('genre'), request.POST.get('sort_by'))
    return JsonResponse(data, safe=False)
