from django.contrib.auth.models import User

# Create your views here.
from django.shortcuts import redirect

from follow_likes_bms.models import Follower


def follow_check(request, subscribe):
    '''Проверка подписан ли человек'''
    user = request.user
    try:
        User.objects.get(user=user, subscribe=subscribe)
        Follower.unfollow()
    except:
        Follower.follow()
    return redirect('home')
