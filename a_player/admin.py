from django.contrib import admin
from a_player.models import FilmModel, CommentModel, TorrentModel


class FilmModelAdmin(admin.ModelAdmin):
    pass


class TorrentModelAdmin(admin.ModelAdmin):
    pass


class CommentModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(FilmModel, FilmModelAdmin)
admin.site.register(CommentModel, CommentModelAdmin)
admin.site.register(TorrentModel, TorrentModelAdmin)
