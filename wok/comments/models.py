from django.db import models

from posts.models import Post
from userprofile.models import Profile
from posts.tasks import count_comments


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name='comments_post')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    time_create = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=600, verbose_name='Текст комментария')
    reply_for = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    # TODO сделать одну модель с FK 'self'

    def __str__(self):
        return f"comment from {self.author} to {self.post.title}"

    def save(self):
        item_id = self.post.__getattribute__('id')
        count_comments.delay(item_id)
        return super().save()
