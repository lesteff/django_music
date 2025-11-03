from django.contrib import admin

from .models import Artist, Album, Song, Genre


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "artist")
    search_fields = ("title",)


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "artist", "album")
    search_fields = ("title",)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
