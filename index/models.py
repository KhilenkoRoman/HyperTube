from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


def user_avatar_path(instance, filename):
	return 'user_avatar/avatar_{0}_{1}'.format(instance.username, filename)


class User(AbstractUser):
	activation_key = models.CharField(max_length=32, blank=True)
	activation_key_time = models.DateTimeField(blank=True, null=True)
	recovery_key = models.CharField(max_length=32, blank=True)
	recovery_key_time = models.DateTimeField(blank=True, null=True)
	avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True, )
