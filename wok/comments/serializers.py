from django.db.models import TextField
from django.shortcuts import get_object_or_404

from .models import Comments
from rest_framework.serializers import ModelSerializer


class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = ('text', 'reply_for')

    def create(self, validated_data):
        obj = Comments.objects.create(**validated_data)
        obj.save(reply_for_id=validated_data['reply_for'])
        return obj

