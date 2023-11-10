from django.http import request, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView

from follow_likes.models import Follower
from userprofile.models import Profile
from userprofile.serializers import ProfileSerializer, ChangePasswordSerializer
from .serializers import SignUpSerializer


# class ProfileDetail(DetailView):
#     """Просмотр профиля пользователя"""
#     model = Profile
#     template_name = 'userprofile/profile.html'
#     context_object_name = 'profile'
#
#     def get_context_data(self, **kwargs):
#         context = super(ProfileDetail, self).get_context_data(**kwargs)
#         try:
#             context['followers'] = Follower.objects.get(subscribe=self.kwargs['id'])
#         except:
#             HttpResponse('Нет подписчиков')
#         return context


class ProfileAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        return Response(ProfileSerializer(profile).data, status=status.HTTP_200_OK)


class MyProfileAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get(self, request):
        # serializer = ProfileSerializer(request.user)
        profile = get_object_or_404(Profile, user=request.user)
        return Response(ProfileSerializer(profile).data, status=status.HTTP_200_OK)
        # return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        profile = get_object_or_404(User, pk=request.user.pk)
        profile.delete()
        return Response(status=status.HTTP_200_OK)

    def patch(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(instance=profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj = self.request.user
        return obj

    def post(self, request):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        # serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password"]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'message': 'Password updated successfully',
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpView(APIView):
    model = Profile
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User(username=serializer.data.get('username'))
        user.set_password(serializer.validated_data.get('password'))
        user.save()
        return Response(status=status.HTTP_201_CREATED)
