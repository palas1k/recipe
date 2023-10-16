from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from comments_answers.serializers import CommentsSerializer
from models import Comments
from posts.models import Post


class CommentsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, pk, request):
        post = get_object_or_404(Post, pk=pk)
        serializer = CommentsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
