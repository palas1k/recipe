from django.shortcuts import render
from django.views.generic import DetailView

from userprofile.models import Profile


class ProfileDetail(DetailView):
    """Просмотр профиля пользователя"""
    model = Profile
    template_name = 'userprofile/profile.html'
    context_object_name = 'profile'
