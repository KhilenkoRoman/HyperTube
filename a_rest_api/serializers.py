from django.contrib.auth.models import Group
from a_user.models import CustomUserModel
from rest_framework import serializers
from a_player.models import FilmModel, TorrentModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ('username', 'first_name', 'last_name', 'email', 'avatar')


class TorrentSerializer(serializers.ModelSerializer):
    quality = serializers.CharField(source='get_quality_display')

    class Meta:
        model = TorrentModel
        fields = ('quality', 'downloaded')


class FilmSerializer(serializers.ModelSerializer):
    torrents = TorrentSerializer(many=True, read_only=True)

    class Meta:
        model = FilmModel
        fields = ('name', 'film_id', 'imdb_id', 'tmd_id', 'torrents')
