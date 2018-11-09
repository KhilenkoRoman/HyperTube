from django.shortcuts import render
import requests
from tempfile import TemporaryFile
import json
import re
from django.core.files import File
from django.utils import timezone
from a_player.models import FilmModel, CommentModel, TorrentModel
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.core.files.temp import NamedTemporaryFile
from a_player.torrent_handler import add_torrent, torrent_info, torrent_status
import cfscrape
from django.conf import settings
import os

# https://localhost:8000/player/3175
# https://localhost:8000/player/7893
# https://localhost:8000/player/3709


def add_torrent_model(film_id, quality):
    quality = int(quality)
    film = FilmModel.objects.get(film_id=film_id)
    if len(TorrentModel.objects.filter(film=film, quality=quality)) == 0:
        torrent = TorrentModel.objects.create(
            film=film,
            quality=quality,
        )
    else:
        torrent = TorrentModel.objects.get(film=film, quality=quality)

    # save torrent file
    if not torrent.torrent_file:
        if not settings.SCRAPER_SESION:
            settings.SCRAPER_SESION = cfscrape.create_scraper()
        film_data = json.loads(film.data)
        r = settings.SCRAPER_SESION.get(film_data['torrents'][quality]['url'])
        if r.status_code != 200:
            return HttpResponse("error " + str(r.status_code))
        temp_file = NamedTemporaryFile(delete=True)
        temp_file.write(r.content)
        temp_file.flush()
        d = r.headers['content-disposition']
        fname = re.findall("filename=(.+)", d)[0].strip('"')
        torrent.torrent_file.save(fname, File(temp_file), save=True)
        torrent.file_name = fname
        torrent.save()

    # add torrent to torrent session
    if not settings.TORRENTS.get(film.film_id + str(quality)):
        add_torrent(torrent)


def player(request, film_id):
    film = FilmModel.objects.filter(film_id=film_id)
    if len(film) == 0:
        return redirect('index')
    film = film[0]
    comments = CommentModel.objects.filter(film=film)

    # search for cast
    if not film.cast:
        flag = False
        url = 'https://api.themoviedb.org/3/find/{}'.format(film.imdb_id)
        params = dict(
            api_key=settings.TMD_API_KEY,
            language='en-US',
            external_source='imdb_id',
        )
        r = requests.get(url=url, params=params)
        if r.status_code == 200:
            tmd_id = r.json()['movie_results'][0]['id']
            url = 'https://api.themoviedb.org/3/movie/{}/credits?'.format(tmd_id)
            params = dict(
                api_key=settings.TMD_API_KEY,
                language='en-US',
            )
            r = requests.get(url=url, params=params)
            if r.status_code == 200:
                cast = r.json()['cast']
                flag = True
        if flag:
            cycle_tag = 0
            cast_len = len(cast)
            if cast_len > 10:
                cast_len = 10
            cast = cast[:cast_len]
            for i in range(len(cast)):
                cast[i]["cycle_tag"] = i % 2
            film.cast = json.dumps(cast)
            film.save()

    if film.cast:
        cast = json.loads(film.cast)
    else:
        cast = None

    context = {'film_id': film_id,
               'comments': comments,
               'film': film,
               'cast': cast,
               'film_data': json.loads(film.data)
               }
    return render(request, 'player/player.html', context)


def ajax_comment(request):
    if request.method != 'POST':
        return HttpResponse("error1")
    if not request.user.is_authenticated:
        return HttpResponse("error2")
    imdb_id = request.POST.get('imdb_id')
    comment = request.POST.get('comment')
    if len(comment) == 0:
        return HttpResponse("error3")
    film = FilmModel.objects.filter(imdb_id=imdb_id)
    if len(film) == 0:
        return HttpResponse("error4")
    CommentModel.objects.create(
        film=film[0],
        user=request.user,
        text=comment,
        date=timezone.now()
    )
    return HttpResponse("sucsess")


def ajax_torr_info(request):
    if request.method != 'POST':
        return HttpResponse("error1")

    film_id = request.POST.get('film_id')
    quality = request.POST.get('quality')

    response = torrent_status(film_id, quality)
    if response['error'] == 1:
        add_torrent_model(film_id, quality)
        response = torrent_status(film_id, quality)

    film = FilmModel.objects.get(film_id=film_id)
    torrent = TorrentModel.objects.get(film=film, quality=quality)

    if response.get("progress") > 0.2 and not torrent.film_file:
        if torrent.quality == 0:
            folder_name = "/video/" + torrent.film.name + "_720p"
        else:
            folder_name = "/video/" + torrent.film.name + "_1080p"

        directry = os.listdir(settings.MEDIA_ROOT + folder_name)
        size = 0
        file_path = ""
        for item in directry:
            tmp_size = os.path.getsize(settings.MEDIA_ROOT + folder_name + "/" + item)
            if tmp_size > size:
                size = tmp_size
                file_path = folder_name + "/" + item
        torrent.film_file = file_path
        torrent.save()

    if torrent.film_file:
        response["film_file"] = torrent.film_file
    else:
        response["film_file"] = ""

    if response.get("progress") == 1:
        torrent.downloaded = True
        torrent.save()

    return JsonResponse(json.dumps(response), safe=False)


def test(request):
    # query_term=""
    # limit=30
    # page=1
    # quality="All"
    # genre=""
    # sort_by="rating"
    # order_by="desc"
    #
    #
    #
    # url = "https://yts.am/api/v2/list_movies.json"
    # params = dict(
    #     query_term=query_term,
    #     limit=limit,
    #     page=page,
    #     quality=quality,
    #     genre=genre,
    #     sort_by=sort_by,
    #     order_by=order_by,
    #     with_rt_ratings=1,
    # )
    #
    # scraper = cfscrape.create_scraper()
    # resp = scraper.get(url=url, params=params)
    # data = resp.json()
    # print(data)

    # https: // localhost: 8000 / player / 3175

    # imdb_id = 'tt0468569'
    # url = 'https://api.themoviedb.org/3/find/{}?api_key={}&language=en-US&external_source=imdb_id'.format(imdb_id, settings.TMD_API_KEY)

    # url = 'https://api.themoviedb.org/3/movie/155/credits?api_key={}&language=ru'.format(settings.TMD_API_KEY)
    #
    # print(requests.get(url).content)

    # print(torrent_status(7893, 0))
    # print(torrent_status(789113, 1))
    # print(requests.get("https://ru.wikipedia.org/wiki/%D0%92%D0%B8%D0%BA%D0%B8"))

    # scraper = cfscrape.create_scraper()
    # print(scraper.get("https://yts.am/api/v2/list_movies.json").content)

    # r = requests.get('http://en.wikipedia.org/wiki/Monty_Python')
    # print(requests.get('http://en.wikipedia.org/wiki/Monty_Python'))
    # data = resp.json()
    # print(data)
    # movie_count = len(data['data']['movies'])
    # if movie_count > 0:
    #     for i in range(movie_count):
    #         if len(FilmModel.objects.filter(imdb_id=data['data']['movies'][i]['imdb_code'])) == 0:
    #             FilmModel.objects.create(
    #                 name=data['data']['movies'][i]['title'],
    #                 imdb_id=data['data']['movies'][i]['imdb_code'],
    #                 film_id=data['data']['movies'][i]['id'],
    #                 data=json.dumps(data['data']['movies'][i]))
    #
    # # print(data['data']['movies'][3])
    # return data

    return HttpResponse("qweqwe")
