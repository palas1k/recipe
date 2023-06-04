from django.db import models

from post_create.models import Post
from userprofile.models import Profile


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name='comments_post')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    time_create = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=600, verbose_name='Текст комментария')


class Reply(models.Model):
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, blank=True, null=True,
                                related_name='reply_comments')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    time_create = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=600, verbose_name='Ответ на комментарий')
