from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Post(models.Model):
    class Meta:
        verbose_name = 'Создать пост'
        verbose_name_plural = 'Создать посты'
    title = models.CharField(max_length=100, help_text='Не более 100 символов', verbose_name='Заголовок')
    slug = models.SlugField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to="images/%Y/%m/%d/", verbose_name='Картинка')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name= 'Дата создания')
    date_updated = models.DateTimeField(auto_now= True, verbose_name='Дата изменения')
    moderated = models.BooleanField(default=False, verbose_name= 'Проверено модерацией')
    is_published = models.BooleanField(default=True, verbose_name= 'Опубликовано')
    draft = models.BooleanField(default=True, verbose_name='Черновик')
    ingredients = models.ForeignKey('Ing', on_delete= models.SET_NULL, verbose_name= 'Ингридиенты', null=True)
    type = models.ForeignKey('Type', verbose_name='Food type', on_delete= models.SET_NULL, null=True)
    group = models.ForeignKey('Group', verbose_name= 'Group of food', on_delete= models.SET_NULL, null = True)
    author = models.ForeignKey(User, on_delete= models.SET_NULL, null=True)
    #comments = models.ManyToManyField()
    reply = models.ForeignKey('self', null = True, related_name= 'reply_ok', on_delete= models.CASCADE)
    likes = models.ManyToManyField(User, related_name='postcomments', blank= True)
    #views =

    def likes_count(self):
        return self.likes.count()

    def reply_count(self):
        return self.reply.count()

    def get_absolute_url(self):
        return reverse('post-view', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Ing(models.Model):
    ing_name = models.CharField(max_length= 100, verbose_name= 'Ингридиенты')
    slug = models.SlugField(max_length=255, unique= True)

    class Meta:
        verbose_name = 'База ингридиентов'
        verbose_name_plural = 'База ингридиентов'
        ordering = ['ing_name']

    def __str__(self):
        return self.ing_name

class Type(models.Model):
    food_type = models.CharField(verbose_name= 'Тип еды', max_length= 255)
    slug = models.SlugField(max_length=255, unique= True)

    def get_absolute_url(self):
        return reverse('type-view', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Тип еды'
        verbose_name_plural = 'Тип еды'

    def __str__(self):
        return self.food_type

class Group(models.Model):
    food_group = models.CharField( verbose_name= 'Группа еды', max_length= 255)
    slug = models.SlugField(max_length=255, unique= True)

    def get_absolute_url(self):
        return reverse('group-view', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Группа еды'
        verbose_name_plural = 'Группа еды'

    def __str__(self):
        return self.food_group
