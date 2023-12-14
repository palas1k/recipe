from django.db.models import TextField

from .models import Comments
from rest_framework.serializers import ModelSerializer


class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = ('text', 'reply_for')
