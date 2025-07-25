from django.urls import path
from . import views


app_name = 'core'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    path('songs/', views.SongListView.as_view(), name='song-list'),
    path('songs/<slug:artist_slug>/<slug:song_slug>/', views.SongDetailView.as_view(), name='song-detail'),

    path('artists/', views.ArtistListView.as_view(), name='artist-list'),
    path('artists/<slug:artist_slug>/', views.ArtistDetailView.as_view(), name='artist-detail'),
]