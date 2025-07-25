from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.utils.text import slugify
from django.db.models import Q

from .mixins import AnonymousRequiredMixin
from core.models import PlayList
from utils import generate_pagination


class UserLoginView(AnonymousRequiredMixin, View):
    template_name = 'accounts/login.html'

    def get(self, request):
        return render(request, self.template_name)
    

class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Successfully Loged Out', 'success')
        return redirect('core:home')


class UserDeleteAccountView(LoginRequiredMixin, View):
    def get(self, request):
        request.user.delete()
        messages.success(request, 'Successfully deleted account', 'success')
        return redirect('core:home')
    

class UserProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        context = {
            'user': request.user,
            'playlists': request.user.get_playlists,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        user = request.user
        playlist_name = request.POST.get('playlist-name')
        slug = slugify(playlist_name)

        if PlayList.objects.filter(user=user, slug=slug).exists():
            messages.error(request, 'This playlist already exists', 'danger')
            return redirect(request.user.get_profile_url)

        PlayList.objects.create(user=user, name=playlist_name, slug=slugify(playlist_name))
        messages.success(request, 'Successfully created playlist', 'success')
        return redirect(request.user.get_profile_url)


class UserPlayListDetailView(LoginRequiredMixin, View):
    template_name = 'accounts/playlist-detail.html'

    def get(self, request, **kwargs):
        playlist = get_object_or_404(PlayList, user=request.user, slug=kwargs['playlist_slug'])
        songs = playlist.songs.filter(is_published=True)

        if request.GET.get('search'):
            songs = songs.filter(Q(name__contains=request.GET['search']) | Q(slug__contains=request.GET['search']))
        
        page_obj = generate_pagination(songs, 50, request)
        
        context = {
            'playlist': playlist,
            'page_obj': page_obj,
        }
        return render(request, self.template_name, context)


class UserPlayListDeleteView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        get_object_or_404(PlayList, user=request.user, slug=kwargs['playlist_slug']).delete()
        messages.success(request, 'Successfully deleted playlist', 'success')
        return redirect(request.user.get_profile_url)