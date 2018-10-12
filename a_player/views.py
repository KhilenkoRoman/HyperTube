from django.shortcuts import render
from django.utils import timezone
from a_player.models import FilmModel, CommentModel
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, render_to_response, redirect


def player(request, film_id):
    film = FilmModel.objects.filter(imdb_id=film_id)
    if len(film) == 0:
        return redirect('index')
    comments = CommentModel.objects.filter(film=film[0])

    context = {'film_id': film_id,
               'comments': comments
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

    # print('--tt0091757--')
    # print('--' + imdb_id.strip('\n') + '--')
    print(film)
    if len(film) == 0:
        return HttpResponse("error4")
    CommentModel.objects.create(
        film=film[0],
        user=request.user,
        text=comment,
        date=timezone.now()
    )
    return HttpResponse("sucsess")
