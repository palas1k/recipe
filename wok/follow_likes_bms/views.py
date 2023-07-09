# Create your views here.
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from follow_likes_bms.models import Follower

# def follow_check(request, subscribe):
#     '''Проверка подписан ли человек'''
#     user = request.user
#     try:
#         User.objects.get(user=user, subscribe=subscribe)
#         Follower.unfollow()
#     except:
#         Follower.follow()
#     return redirect('home')
from userprofile.models import Profile


def follow(request, pk):
    """User кто подписывается, subscribe на кого подписываются"""
    user = request.user.profile
    follow_to = get_object_or_404(Profile, pk=pk)
    Follower.objects.create(user=user, subscribe=follow_to)
    return redirect('profile-view', pk=follow_to.id)
