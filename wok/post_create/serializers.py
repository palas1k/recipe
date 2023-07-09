from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.serializers import ModelSerializer, CharField

from .models import Post, PostContent
from userprofile.serializers import UserSerializer


class PostContentSerializer(ModelSerializer):
    class Meta:
        model = PostContent
        fields = '__all__'


class PostSerializer(ModelSerializer):
    post_content = PostContentSerializer(many=True, source='post')
    queryset = Post.objects.prefetch_related('post').all()

    class Meta:
        model = Post
        fields = '__all__'


class AllPostsSerializer(ModelSerializer):
    author_name = CharField(source='author.username', read_only=True)
    food_type = CharField(source='type.food_type', read_only=True)
    food_group = CharField(source='group.food_group', read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'date_updated', 'author_name', 'food_type', 'food_group')
