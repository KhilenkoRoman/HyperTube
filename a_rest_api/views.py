from a_user.models import CustomUserModel
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from a_rest_api.serializers import UserSerializer, FilmSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from a_player.models import FilmModel


@api_view(['GET'])
def user_list(request, format=None):
    """
    List all users
    params: username , first_name, last_name, email
    """

    if request.method == 'GET':
        users = CustomUserModel.objects.all()
        if request.GET.get('username'):
            users = users.filter(username=request.GET['username'])
        if request.GET.get('first_name'):
            users = users.filter(first_name=request.GET['first_name'])
        if request.GET.get('last_name'):
            users = users.filter(last_name=request.GET['last_name'])
        if request.GET.get('email'):
            users = users.filter(email=request.GET['email'])

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def film_list(request, format=None):
    """
    List all films
    params: downloaded[True, False], name, imdb_id
    """

    if request.method == 'GET':
        films = FilmModel.objects.all()
        if request.GET.get('downloaded'):
            if request.GET['downloaded'] == 'True':
                films = films.filter(torrents__downloaded=True)
            elif request.GET['downloaded'] == 'False':
                films = films.filter(torrents__downloaded=False)
        if request.GET.get('name'):
            films = films.filter(name=request.GET['name'])
        if request.GET.get('imdb_id'):
            films = films.filter(imdb_id=request.GET['imdb_id'])

        serializer = FilmSerializer(films, many=True)
        return Response(serializer.data)
