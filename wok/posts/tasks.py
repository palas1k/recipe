from celery import shared_task
from django.shortcuts import get_object_or_404


@shared_task
def count_comments(item_id):
    '''
    Подсчет кол-ва комментариев под постом
    :param item_id: int
    :return: None
    '''
    from .models import Post
    post = get_object_or_404(Post, pk=item_id)
    comm_sum = post.comments_post.count()
    post.count_comments = comm_sum
    post.save()


@shared_task
def count_likes(post_id):
    '''
    Подсчет кол-ва лайков под постом
    :param post_id: int
    :return:
    '''
    from .models import Post
    post = get_object_or_404(Post, pk=post_id)
    likes_count = post.like_set.count()
    post.count_likes = likes_count
    post.save()


@shared_task
def count_view(post_id):
    '''
    Подсчет просмотров поста
    :param post_id:
    :return:
    '''
    from .models import Post
    post = get_object_or_404(Post, pk=post_id)
    if post.count_views is None:
        post.count_views = 1
    else:
        post.count_views += 1
    post.save(update_fields=('count_views',))
