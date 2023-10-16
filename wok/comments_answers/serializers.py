from models import Comments
from rest_framework.serializers import ModelSerializer


class CommentsSerializer(ModelSerializer):
    model = Comments
    fields = ('text',)
