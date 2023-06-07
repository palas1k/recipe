from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from userprofile.models import Profile


class Follower(models.Model):
    '''Модель подписчиков'''
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owner')
    subscribe = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='subscribe')

    def __str__(self):
        return f'{self.user} подписан на {self.subscribe} '

    def follow(self, user, subscribe):
        Follower.objects.create(user=user, subscribe=subscribe)

    def unfollow(self, user, subscribe):
        follower = Follower.objects.get(user=user, subscribe=subscribe)
        follower.delete()


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='likes')
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    User = get_user_model()

    def add_like(obj, user):
        obj_type = ContentType.objects.get_for_model(obj)
        like, is_created = Like.objects.get_or_create(content_type=obj_type, object_id=obj.id, user=user)
        return like

    def remove_like(obj, user):
        obj_type = ContentType.objects.get_for_model(obj)
        Like.objects.filter(content_type=obj_type, object_id=obj.id, user=user).delete()

    def is_fan(obj, user) -> bool:
        """Проверяет, лайкнул ли user obj"""
        if not user.is_authenticated:
            return False
        obj_type = ContentType.objects.get_for_model(obj)
        likes = Like.objects.filter(content_type=obj_type, object_id=obj.id, user=user)
        return likes.exists()

    def get_likers(obj, user):
        """Все пользователи лайкнувшие obj"""
        obj_type = ContentType.objects.get_for_model(obj)
        return User.objects.filter(likes__content_type=obj_type, likes__objects_id=obj.id)
