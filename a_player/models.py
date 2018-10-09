from django.db import models
from a_user.models import CustomUserModel


class FilmModel(models.Model):
    name = models.CharField(max_length=200)
    imdb_id = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class CommentModel(models.Model):
    film = models.ForeignKey(FilmModel, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + "_comment"
