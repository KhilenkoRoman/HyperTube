from django.db import models
import shutil
import os
from django.conf import settings
from a_user.models import CustomUserModel
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver


class FilmModel(models.Model):
    name = models.CharField(max_length=200)
    film_id = models.CharField(max_length=32, unique=True)
    imdb_id = models.CharField(max_length=32, unique=True)
    tmd_id = models.CharField(max_length=64, blank=True, null=True)
    data = models.TextField()
    cast = models.TextField(blank=True, null=True)
    ru_info = models.TextField(blank=True, null=True)
    cover = models.ImageField(upload_to="covers", blank=True, null=True)
    en_sub_srt = models.FileField(upload_to="subtitles", blank=True, null=True)
    ru_sub_srt = models.FileField(upload_to="subtitles", blank=True, null=True)
    en_sub_vtt = models.CharField(max_length=512, blank=True, null=True)
    ru_sub_vtt = models.CharField(max_length=512, blank=True, null=True)

    def __str__(self):
        return self.name


class FilmHistoryModel(models.Model):
    film = models.ForeignKey(FilmModel, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + "_history"


def torrent_path(instance, filename):
    return 'torrent_files/{0}'.format(filename)


class TorrentModel(models.Model):
    quality_choises = (
        (0, '720p'),
        (1, '1080p'),
    )
    file_name = models.CharField(max_length=200, null=True)
    film = models.ForeignKey(FilmModel, on_delete=models.CASCADE)
    date = models.DateTimeField(blank=True, null=True)
    torrent_file = models.FileField(upload_to=torrent_path, blank=True, null=True)
    film_file = models.CharField(max_length=420, blank=True, null=True)
    quality = models.DecimalField(max_digits=1, decimal_places=0, choices=quality_choises)
    downloaded = models.BooleanField(default=False)

    def __str__(self):
        return self.film.name


# @receiver(post_delete, sender=TorrentModel)
# def handle_files_on_delete(sender, instance, **kwargs):
#     dirpath = os.path.join(settings.MEDIA_ROOT, 'video', instance.film.name + ("_720p" if instance.quality == 0 else "_1080p"))
#     if os.path.exists(dirpath) and os.path.isdir(dirpath):
#         shutil.rmtree(dirpath)


class CommentModel(models.Model):
    film = models.ForeignKey(FilmModel, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + "_comment"
