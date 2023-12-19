from django.shortcuts import redirect, get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from follow_likes.models import Follower
from userprofile.models import Profile
from userprofile.serializers import ProfileSerializer


class FollowAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        Follower.objects.create(user=request.user, subscribe_id=pk)
        user = Profile.objects.get(pk=pk)
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        folow = get_object_or_404(Follower, subscribe_id=pk)
        user = Profile.objects.get(pk=pk)
        folow.delete()
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

