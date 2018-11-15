from django.core.management.base import BaseCommand, CommandError
from a_player.models import TorrentModel
from django.utils import timezone
import datetime


class Command(BaseCommand):
    help = "Deleting movies that hasn't been reviewed for 1 month"

    def handle(self, *args, **options):
        print("---")
        for film in TorrentModel.objects.all():
            if film.date < timezone.now() - datetime.timedelta(weeks=+4):
                print(film.film.name + (" 720p" if film.quality == 0 else " 1080p") + " deleted")
                print("---")
                film.delete()