from django.shortcuts import render
import requests
from tempfile import TemporaryFile
import json
import re
from django.core.files import File
from django.utils import timezone
from a_player.models import FilmModel, CommentModel, TorrentModel, FilmHistoryModel
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.core.files.temp import NamedTemporaryFile
from a_player.torrent_handler import add_torrent, torrent_info, torrent_status
import cfscrape
from django.conf import settings
import os
import webvtt


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
            date=timezone.now()
        )
    else:
        torrent = TorrentModel.objects.get(film=film, quality=quality)
        torrent.date = timezone.now()
        torrent.save()

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


def search_subs(film, lang):
    url = 'https://subtitle-api.org/videos/{}/subtitles'.format(film.imdb_id)
    params = dict(
        lang=lang,
        format="SUBRIP",
    )
    r = requests.get(url=url, params=params)
    if r.status_code != 200:
        return
    resp = json.loads(r.text)

    for item in resp['items']:
        url = 'https://subtitle-api.org/videos/{}/subtitles/{}'.format(film.imdb_id, item['id'])
        r = requests.get(url=url, params=params)
        if r.status_code != 200:
            continue
        temp_file = NamedTemporaryFile(delete=True)
        temp_file.write(r.content)
        temp_file.flush()

        if lang == "ru":
            film.ru_sub_srt.save(film.imdb_id + "_ru.srt", File(temp_file), save=True)
            webvtt.from_srt(settings.MEDIA_ROOT + '/' + str(film.ru_sub_srt)).save()
            film.ru_sub_vtt = film.imdb_id + "_ru.vtt"
            film.save()
        else:
            film.en_sub_srt.save(film.imdb_id + "_en.srt", File(temp_file), save=True)
            webvtt.from_srt(settings.MEDIA_ROOT + '/' + str(film.en_sub_srt)).save()
            film.en_sub_vtt = film.imdb_id + "_en.vtt"
            film.save()
        return


def get_tmd_id(film):
    if film.tmd_id:
        return film.tmd_id
    url = 'https://api.themoviedb.org/3/find/{}'.format(film.imdb_id)
    params = dict(
        api_key=settings.TMD_API_KEY,
        language='en-US',
        external_source='imdb_id',
    )
    r = requests.get(url=url, params=params)
    if r.status_code == 200:
        tmd_id = r.json()['movie_results'][0]['id']
        film.tmd_id = tmd_id
        film.save()
        return tmd_id
    else:
        return None


def seach_cast(film):
    tmd_id = get_tmd_id(film)
    if not tmd_id:
        return None

    url = 'https://api.themoviedb.org/3/movie/{}/credits?'.format(tmd_id)
    params = dict(
        api_key=settings.TMD_API_KEY,
        language='en-US',
    )
    r = requests.get(url=url, params=params)
    if r.status_code == 200:
        cast = r.json()['cast']
        cast_len = len(cast)
        if cast_len > 10:
            cast_len = 10
        cast = cast[:cast_len]
        for i in range(len(cast)):
            cast[i]["cycle_tag"] = i % 2
        film.cast = json.dumps(cast)
        film.save()
        return cast
    else:
        return None


def rus_info_search(film):
    tmd_id = get_tmd_id(film)
    if not tmd_id:
        return None

    url = 'https://api.themoviedb.org/3/movie/{}?'.format(tmd_id)
    params = dict(
        api_key=settings.TMD_API_KEY,
        language='ru',
    )
    r = requests.get(url=url, params=params)
    if r.status_code == 200:
        ru_info = r.json()
        film.ru_info = json.dumps(ru_info)
        film.save()
        return ru_info
    return None


def player(request, film_id):
    if request.user.id is None:
        return redirect('index')
    film = FilmModel.objects.filter(film_id=film_id)
    if len(film) == 0:
        return redirect('index')
    film = film[0]
    comments = CommentModel.objects.filter(film=film)

    if not film.en_sub_vtt:
        search_subs(film, 'en')
    if not film.ru_sub_vtt:
        search_subs(film, 'ru')

    if film.cast:
        cast = json.loads(film.cast)
    else:
        cast = seach_cast(film)

    ru_info = None
    if request.session["lang"] == 2:
        if film.ru_info:
            ru_info = json.loads(film.ru_info)
        else:
            ru_info = rus_info_search(film)

    film_data = json.loads(film.data)
    get_720p = False
    get_1080p = False
    if film_data.get('torrents'):
        for i in film_data['torrents']:
            if i.get('quality') == '720p':
                get_720p = True
            if i.get('quality') == '1080p':
                get_1080p = True
    context = {'film_id': film_id,
               'comments': comments,
               'film': film,
               'cast': cast,
               'film_data': film_data,
               'get_720p': get_720p,
               'get_1080p': get_1080p,
               'ru_info': ru_info,
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
    newcomment = CommentModel.objects.create(
        film=film[0],
        user=request.user,
        text=comment,
        date=timezone.now()
    )
    return HttpResponse(str(newcomment.id))


def ajax_del_comment(request):
    if request.method != 'POST':
        return HttpResponse("error1")
    if not request.user.is_authenticated:
        return HttpResponse("error2")
    imdb_id = request.POST.get('imdb_id')
    comment_id = request.POST.get('commentId')
    film = FilmModel.objects.filter(imdb_id=imdb_id)
    # user = CommentModel.objects.filter(pk=comment_id, user=request.user)
    # if len(user) == 0:
    #     return HttpResponse("error4")
    if len(film) == 0:
        return HttpResponse("error5")
    CommentModel.objects.filter(pk=comment_id).delete()
    return HttpResponse("success")

def ajax_edit_comment(request):
    if request.method != 'POST':
        return HttpResponse("error1")
    if not request.user.is_authenticated:
        return HttpResponse("error2")
    imdb_id = request.POST.get('imdb_id')
    commentId = request.POST.get('commentId')
    commentText = request.POST.get('commentText')
    film = FilmModel.objects.filter(imdb_id=imdb_id)
    if len(film) == 0:
        return HttpResponse("error4")
    comm = CommentModel.objects.get(pk=commentId)
    comm.text = commentText
    comm.save()
    return HttpResponse("success")


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

    if len(FilmHistoryModel.objects.filter(film=film, user=request.user)) == 0:
        FilmHistoryModel.objects.create(film=film, user=request.user)

    thr = settings.TORRENT_DOWNLOAD_THRETHOSLD
    if type(thr) != float or thr > 1 or thr < 0.05:
        thr = 0.05

    if response.get("progress") > thr and not torrent.film_file:
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
