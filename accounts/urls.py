from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('delete-account/', views.UserDeleteAccountView.as_view(), name='delete-account'),

    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/<slug:playlist_slug>/', views.UserPlayListDetailView.as_view(), name='playlist-detail'),
    path('profile/<slug:playlist_slug>/delete/', views.UserPlayListDeleteView.as_view(), name='playlist-delete'),
]