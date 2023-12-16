from django.contrib.auth.models import User, AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Profile(AbstractUser):
    """Модель профиля пользователя"""
    avatar = models.ImageField('Аватар', upload_to='profile/', blank=True, null=True,
                               validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])])

    @property
    def is_authenticated(self):
        '''Вседа возвращает True. Способ узнать был ли пользователь аутентифицирован'''
        return True

    def __str__(self):
        return self.username


    class Meta():
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
