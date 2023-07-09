from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Profile(models.Model):
    """Модель профиля пользователя"""
    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='profileuser')
    avatar = models.ImageField('Аватар', upload_to='profile/', blank=True, null=True,
                               validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])])

    @property
    def is_authenticated(self):
        '''Вседа возвращает True. Способ узнать был ли пользователь аутентифицирован'''
        return True

    def __str__(self):
        return self.user.username

    # def get_absolute_url(self):
    #     return reverse("profile-view", kwargs={'pk': self.pk})

    class Meta():
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создание профиля при регистрации"""
    if created:
        Profile.objects.create(user=instance)


@receiver
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
