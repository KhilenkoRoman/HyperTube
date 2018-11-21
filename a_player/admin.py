from django.contrib import admin
from a_player.models import FilmModel, CommentModel, TorrentModel, FilmHistoryModel


class FilmModelAdmin(admin.ModelAdmin):
    search_fields = ['name']
    pass


class TorrentModelAdmin(admin.ModelAdmin):
    pass


class CommentModelAdmin(admin.ModelAdmin):
    pass


class FilmHistoryModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(FilmModel, FilmModelAdmin)
admin.site.register(CommentModel, CommentModelAdmin)
admin.site.register(TorrentModel, TorrentModelAdmin)
admin.site.register(FilmHistoryModel, FilmHistoryModelAdmin)
