from django.contrib import admin

from follow_likes_bms.models import Like, Follower
from userprofile.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Профиль пользователя"""
    list_display = ['user', ]


@admin.register(Like)
class ProfileAdmin(admin.ModelAdmin):
    """Лайки"""
    list_display = ['user', ]


admin.site.register(Follower)