from django.contrib import admin
from django.utils.translation import ngettext
from django.contrib import messages

from .models import Artist, Song, PlayList


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    list_max_show_all = 200
    list_per_page = 20
    prepopulated_fields = {'slug': ['name']}
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['id', 'artist', 'name', 'is_published', 'created_at', 'updated_at']
    list_filter = ['artist', 'is_published', 'created_at', 'updated_at']
    list_max_show_all = 200
    list_per_page = 20
    prepopulated_fields = {'slug': ['name']}
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['publish', 'unpublish']

    def publish(self, request, queryset):
        """ To publish selected songs """
        updated = queryset.update(is_published=True)
        self.message_user(
            request,
            ngettext(
                f"Successfully published {updated} song.",
                f"Successfully published {updated} songs.",
                updated,
            ),
            messages.SUCCESS,
        )
    publish.short_description = 'Publish selected songs'

    def unpublish(self, request, queryset):
        """ To unpublish selected songs """
        updated = queryset.update(is_published=False)
        self.message_user(
            request,
            ngettext(
                f"Successfully unpublished {updated} song.",
                f"Successfully unpublished {updated} songs.",
                updated,
            ),
            messages.SUCCESS,
        )
    unpublish.short_description = 'Unpublish selected songs'


@admin.register(PlayList)
class PlayListAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'created_at', 'updated_at']
    list_filter = ['user', 'created_at', 'updated_at']
    list_max_show_all = 200
    list_per_page = 20
    prepopulated_fields = {'slug': ['name']}
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']
