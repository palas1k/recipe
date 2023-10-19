from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from comments.serializers import CommentsSerializer
from userprofile.models import Profile
from .models import Comments
from posts.models import Post


class CommentsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentsSerializer

    def get(self, request, pk):
        comments = Comments.objects.filter(post_id=pk)
        return Response(CommentsSerializer(comments, many=True).data, status=status.HTTP_200_OK)

    # @extend_schema(parameters=[OpenApiParameter('reply_id', int)])
    def post(self, request, pk, reply_id):
        _user = Profile.objects.get(user=request.user)
        serializer = CommentsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            author=_user,
            post_id=pk,
            reply_for_id=reply_id,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # TODO логин переписать через профайл


class CommentsRetrieveAPIView(APIView):
    serializer_class = CommentsSerializer

    # permission_classes = []

    def delete(self, request, pk):
        comment = get_object_or_404(Comments, pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        comment = get_object_or_404(Comments, pk=pk)
        serializer = CommentsSerializer(instance=comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
