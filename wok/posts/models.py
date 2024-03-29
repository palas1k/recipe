from django.db import models
from django.urls import reverse

from userprofile.models import Profile


class Post(models.Model):
    '''Модель поста'''

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    title = models.CharField(max_length=100, help_text='Не более 100 символов', verbose_name='Заголовок')
    slug = models.SlugField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    moderated = models.BooleanField(default=False, verbose_name='Проверено модерацией')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    draft = models.BooleanField(default=True, verbose_name='Черновик')
    ingredients = models.ManyToManyField('Ing', verbose_name='Ингридиенты')
    type = models.ForeignKey('Type', verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey('Group', verbose_name='Group of food', on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    count_likes = models.IntegerField(null=True, blank=True)
    count_views = models.IntegerField(null=True, blank=True)
    count_comments = models.IntegerField(null=True, blank=True)

    # TODO подсчет комментариев под постом +celery
    #  подсчет лайков под постом
    #  подсчет просмотров

    # для получения контента связанного с постом
    def get_all_postcontent(self):
        return PostContent.objects.filter(post=self.pk)

    def get_absolute_url(self):
        return reverse('post-view', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Ing(models.Model):
    '''Ингридиенты'''
    ing_name = models.CharField(max_length=100, verbose_name='Ингридиенты')
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'База ингридиентов'
        verbose_name_plural = 'База ингридиентов'
        ordering = ['ing_name']

    def __str__(self):
        return self.ing_name


class Type(models.Model):
    '''Тип еды'''
    food_type = models.CharField(verbose_name='Тип еды', max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def get_absolute_url(self):
        return reverse('type-view', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Тип еды'
        verbose_name_plural = 'Тип еды'

    def __str__(self):
        return self.food_type


class Group(models.Model):
    '''Группировка еды'''
    food_group = models.CharField(verbose_name='Группа еды', max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def get_absolute_url(self):
        return reverse('group-view', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Группа еды'
        verbose_name_plural = 'Группа еды'

    def __str__(self):
        return self.food_group


# class PostImage(models.Model):
#     image = models.ImageField(upload_to="images/%Y/%m/%d/", verbose_name='Картинка', blank=True)
#
#     class Meta:
#         verbose_name = 'Изображение'
#         verbose_name_plural = 'Изображения'

class PostContent(models.Model):
    '''Контентная часть поста'''
    text = models.TextField(max_length=500)
    image = models.ImageField(upload_to="images/%Y/%m/%d/", verbose_name='Картинка', blank=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post')

    def __str__(self):
        return self.text
