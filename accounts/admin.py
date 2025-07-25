from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('email', 'is_active', 'is_admin', 'is_staff',)
    list_filter = ('email', 'is_active', 'is_admin',)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    fieldsets = (
        ('User Info', {'fields': ('email', 'password',)}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'last_login',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2',)}),
    )


admin.site.unregister(Group)