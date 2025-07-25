from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.urls import reverse

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin

    @property
    def get_profile_url(self):
        return reverse('accounts:profile')
    
    @property
    def get_logout_url(self):
        return reverse('accounts:logout')
    
    @property
    def get_delete_account_url(self):
        return reverse('accounts:delete-account')

    @property
    def get_playlists_url(self):
        return reverse('accounts:playlists')
    
    @property
    def get_playlists(self):
        return self.playlists.all()
    
    @property
    def get_new_playlist_url(self):
        return reverse('accounts:new-playlist')