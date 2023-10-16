from django.contrib import admin

from posts.models import *


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'moderated']
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Ing)
class IngAdmin(admin.ModelAdmin):
    list_display = ['ing_name', ]
    prepopulated_fields = {"slug": ("ing_name",)}


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['food_type']
    prepopulated_fields = {"slug": ("food_type",)}


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['food_group']
    prepopulated_fields = {"slug": ("food_group",)}


@admin.register(PostContent)
class PostContentAdmin(admin.ModelAdmin):
    list_display = ['text']
