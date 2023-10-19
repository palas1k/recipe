from django.db.models import TextField

from .models import Comments
from rest_framework.serializers import ModelSerializer, IntegerField


class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = ('text',)
