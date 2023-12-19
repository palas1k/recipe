from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import redirect

from posts.models import Post
from userprofile.models import Profile
from posts.tasks import count_likes


class Follower(models.Model):
    '''Модель подписчиков'''
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owner')
    subscribe = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='subscribe')
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_time',)

    def __str__(self):
        return f'{self.user} подписан на {self.subscribe}'

    def follow_check(request, pk):
        '''Проверка подписан ли человек'''
        try:
            User.objects.get(user=request.user, subscribe_id=pk)
            return True
        except:
            return False


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='like_post')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def save(self):
        item_id = self.post.__getattribute__('id')
        count_likes.delay(item_id)
        return super().save()
