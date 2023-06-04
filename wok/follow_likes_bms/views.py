from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

# Create your views here.
from follow_likes_bms.models import Like

User = get_user_model()


# or get_user


def add_like(obj, user):
    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = Like.objects.get_or_create(content_type=obj_type, object_id=obj.id, user=user)
    return like
