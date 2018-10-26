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
from a_player.torrent_handler import add_torrent, torrent_info


# https://localhost:8000/player/3175
# https://localhost:8000/player/7893

def player(request, film_id):
    film = FilmModel.objects.filter(film_id=film_id)
    if len(film) == 0:
        return redirect('index')
    film = film[0]
    comments = CommentModel.objects.filter(film=film)
    data = json.loads(film.data)
    quality = 0

    # save torrent file
    if len(TorrentModel.objects.filter(film=film, quality=quality)) == 0:
        torrent = TorrentModel.objects.create(
            film=film,
            quality=quality,
        )
    else:
        torrent = TorrentModel.objects.get(film=film, quality=quality)

    if not torrent.torrent_file:
        r = requests.get(data['torrents'][quality]['url'])
        temp_file = NamedTemporaryFile(delete=True)
        temp_file.write(r.content)
        temp_file.flush()
        d = r.headers['content-disposition']
        fname = re.findall("filename=(.+)", d)[0].strip('"')
        torrent.torrent_file.save(fname, File(temp_file), save=True)
        torrent.file_name = fname
        torrent.save()

    add_torrent(torrent)

    context = {'film_id': film_id,
               'comments': comments,
               'title': data['title'],
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


def test(request):
    torrent_info()
    return HttpResponse("qweqwe")
