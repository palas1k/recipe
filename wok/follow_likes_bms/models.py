from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from userprofile.models import Profile


class Follower(models.Model):
    '''Модель подписчиков'''
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owner')
    subscriber = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='subscriber')

    def __str__(self):
        return f'{self.subscriber} подписан на {self.user}'


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='likes')
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
