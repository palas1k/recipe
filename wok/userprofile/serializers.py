from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.serializers import ModelSerializer, Serializer, ValidationError

from userprofile.models import Profile


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class ProfileSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ('avatar', 'user')


class ChangePasswordSerializer(Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class SignUpSerializer(Serializer):
    '''
    вылетает ошибка 500 но работает
    '''
    # avatar = serializers.ImageField(required=False, allow_null=True)
    username = serializers.CharField(max_length=31)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    model = User

    def validate_password2(self, password2):
        if self.initial_data.get('password') != password2:
            raise ValidationError('Пароли не совпадают')
        return password2
