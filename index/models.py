from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	recovery_key = models.CharField(max_length=30, blank=True)
	recovery_key_time = models.DateTimeField(blank=True, null=True)
	avatar = models.ImageField(upload_to='media/user_avatar', blank=True, null=True, )
