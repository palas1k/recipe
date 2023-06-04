from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from .forms import *
from .models import Post


class PostsList(ListView):
    model = Post
    template_name = 'post_create/index.html'
    context_object_name = 'foodrecipe_post_posts'
    queryset = Post.objects.filter(is_published=True, moderated=True).order_by('-date_created')

    # def get_queryset(self):
    #    user = get_object_or_404(User, username = self.kwargs.get('username'))
    #    return Post.objects.filter(author = user).order_by('-date_created')


class CreatePost(CreateView):
    template_name = 'post_create/addpage.html'
    model = Post
    form_class = PostForm
    success_url = ''

    def get(self, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        post_content_form = PostContentFormset()
        return self.render_to_response(self.get_context_data(form=form, post_content_form=post_content_form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        post_content_form = PostContentFormset(self.request.POST, self.request.FILES)
        self.object = form.save()
        post_content_form.instance = self.object
        post_content_form.cleaned_data
        post_content_form.save()
        return HttpResponseRedirect(reverse('home'))


class PostView(DetailView):
    model = Post
    template_name = 'post_create/postdetail.html'
    context_object_name = 'post'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['post_content'] = PostContent.objects.filter(post_id = Post.id)
