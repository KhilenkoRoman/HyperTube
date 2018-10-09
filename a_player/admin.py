from django.contrib import admin
from a_player.models import FilmModel, CommentModel


class FilmModelAdmin(admin.ModelAdmin):
    pass


class CommentModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(FilmModel, FilmModelAdmin)
admin.site.register(CommentModel, CommentModelAdmin)
