from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'bio',
        'role',
    )
    list_filter = (
        'email',
        'username',
        'role',
    )
