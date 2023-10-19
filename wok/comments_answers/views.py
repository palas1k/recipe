from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from comments_answers.serializers import CommentsSerializer
from userprofile.models import Profile
from .models import Comments
from posts.models import Post


class CommentsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentsSerializer

    def get(self, pk, request):
        comments = Comments.objects.filter(post=pk, author=request.user)
        return Response(CommentsSerializer(comments, many=True).data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        _user = Profile.objects.get(user=request.user)
        serializer = CommentsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reply_id = serializer.validated_data.get('reply_for')
        serializer.save(
            author=_user,
            post_id=pk,
            reply_for=reply_id,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # TODO логин переписать через профайл
