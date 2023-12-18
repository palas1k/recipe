from django.db.models import TextField
from django.shortcuts import get_object_or_404

from userprofile.models import Profile
from .models import Comments
from rest_framework.serializers import ModelSerializer


class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = ('text', 'reply_for', 'time_create')
