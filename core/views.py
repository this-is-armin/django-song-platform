from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Artist, Song
from .forms import AddToPlayListForm
from utils import generate_pagination


class HomeView(View):
    template_name = 'main/index.html'

    def get(self, request):
        return render(request, self.template_name)


class SongListView(View):
    template_name = 'songs/list.html'

    def get(self, request):
        songs = Song.objects.filter(is_published=True)

        if request.GET.get('search'):
            songs = songs.filter(Q(name__contains=request.GET['search']) | Q(slug__contains=request.GET['search']))
        
        page_obj = generate_pagination(songs, 50, request)

        context = {
            'page_obj': page_obj,
        }
        return render(request, self.template_name, context)


class SongDetailView(View):
    template_name = 'songs/detail.html'
    form_class = AddToPlayListForm

    def setup(self, request, *args, **kwargs):
        self.artist_instance = get_object_or_404(Artist, slug=kwargs['artist_slug'])
        self.song_instance = get_object_or_404(Song, artist=self.artist_instance, slug=kwargs['song_slug'], is_published=True)
        return super().setup(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        form = self.form_class(request.user) if request.user.is_authenticated else None

        context = {
            'song': self.song_instance,
            'form': form,
        }
        return render(request, self.template_name, context)
    
    @method_decorator(login_required)
    def post(self, request, **kwargs):
        form = self.form_class(request.user, request.POST)

        if form.is_valid():
            playlist = form.cleaned_data['playlist']

            if playlist.songs.filter(pk=self.song_instance.pk).exists():
                messages.error(request, 'This song already exists in the playlist', 'danger')
            else:
                playlist.songs.add(self.song_instance)
                messages.success(request, 'Successfully added song to playlist', 'success')
            return redirect(self.song_instance.get_absolute_url)
        context = {
            'song': self.song_instance,
            'form': form(request.user),
        }
        return render(request, self.template_name, context)


class ArtistListView(View):
    template_name = 'artists/list.html'

    def get(self, request):
        artists = Artist.objects.all()

        if request.GET.get('search'):
            artists = artists.filter(Q(name__contains=request.GET['search']) | Q(slug__contains=request.GET['search']))
        
        page_obj = generate_pagination(artists, 50, request)

        context = {
            'page_obj': page_obj,
        }
        return render(request, self.template_name, context)


class ArtistDetailView(View):
    template_name = 'artists/detail.html'

    def get(self, request, **kwargs):
        artist = get_object_or_404(Artist, slug=kwargs['artist_slug'])
        songs = artist.get_songs_list

        if request.GET.get('search'):
            songs = songs.filter(Q(name__contains=request.GET['search']) | Q(slug__contains=request.GET['search']))

        context = {
            'artist': artist,
            'songs': songs,
        }
        return render(request, self.template_name, context)