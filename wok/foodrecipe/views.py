from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from foodrecipe.models import Post


class PostsList(ListView):
    model = Post
    #template_name =
    context_object_name = 'foodrecipe_post_posts'

