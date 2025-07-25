from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.conf import settings

import os


def generate_artist_image_path(instance, filename):
    filename = f"{instance.slug}{os.path.splitext(filename)[1]}"
    file_path = f"artists/images/{instance.slug}/{filename}"
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    
    if os.path.exists(full_path):
        os.remove(full_path)

    return file_path

def generate_song_image_path(instance, filename):
    filename = f"{instance.slug}{os.path.splitext(filename)[1]}"
    file_path = f"songs/images/{instance.artist.slug}/{filename}"
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    
    if os.path.exists(full_path):
        os.remove(full_path)

    return file_path

def generate_song_audio_file_path(instance, filename):
    filename = f"{instance.slug}{os.path.splitext(filename)[1]}"
    file_path = f"songs/audio_files/{instance.artist.slug}/{filename}"
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    
    if os.path.exists(full_path):
        os.remove(full_path)

    return file_path


class Artist(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(
        upload_to=generate_artist_image_path,
        blank=True, 
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

    # URL Properties
    @property
    def get_absolute_url(self):
        return reverse('core:artist-detail', args=[self.slug])
    
    # List Properties
    @property
    def get_songs_list(self):
        return self.songs.filter(is_published=True)


class Song(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(
        upload_to=generate_song_image_path, 
        blank=True, 
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])]
    )
    audio_file = models.FileField(
        upload_to=generate_song_audio_file_path, 
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav'])]
    )
    description = models.TextField(blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['artist', 'slug'],
                name='unique_song_slug_per_artist',
            )
        ]
    
    def __str__(self):
        return f"{self.artist} - {self.name}"
    
    def clean(self):
        super().clean()

        if Song.objects.filter(artist=self.artist, slug=self.slug).exclude(pk=self.pk).exists():
            raise ValidationError(
                {'slug': 'This slug already exists for this artist.'}
            )
    
    # URL Properties
    @property
    def get_absolute_url(self):
        return reverse('core:song-detail', args=[self.artist.slug, self.slug])


class PlayList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='playlists')
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    songs = models.ManyToManyField(Song, blank=True, related_name='playlists')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    # URL Properties
    @property
    def get_absolute_url(self):
        return reverse('accounts:playlist-detail', args=[self.slug])
    
    @property
    def get_delete_url(self):
        return reverse('accounts:playlist-delete', args=[self.slug])