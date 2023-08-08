from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Post, PostContent
from .serializers import AllPostsSerializer, PostSerializer, CreatePostSerializer, PostContentSerializer
from .pagination import Pagination


# class PostsList(ListView):
#     model = Post
#     template_name = 'post_create/index.html'
#     context_object_name = 'foodrecipe_post_posts'
#     queryset = Post.objects.filter(is_published=True, moderated=True).order_by('-date_created')

# def get_queryset(self):
#    user = get_object_or_404(User, username = self.kwargs.get('username'))
#    return Post.objects.filter(author = user).order_by('-date_created')


# class CreatePost(CreateView):
#     template_name = 'post_create/addpage.html'
#     model = Post
#     form_class = PostForm
#     success_url = ''
#
#     def get(self, *args, **kwargs):
#         self.object = None
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         post_content_form = PostContentFormset()
#         return self.render_to_response(self.get_context_data(form=form, post_content_form=post_content_form))
#
#     def post(self, request, *args, **kwargs):
#         self.object = None
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         post_content_form = PostContentFormset(self.request.POST, self.request.FILES)
#         self.object = form.save()
#         post_content_form.instance = self.object
#         post_content_form.cleaned_data
#         post_content_form.save()
#         return HttpResponseRedirect(reverse('home'))
#
#
# class PostView(DetailView):
#     model = Post
#     template_name = 'post_create/postdetail.html'
#     context_object_name = 'post'


# class PostsAPIView(ListAPIView):
#     serializer_class = PostSerializer
#     queryset = Post.objects.all()
#
class PostRetrieveAPIView(APIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        return Response(PostSerializer(post).data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(status=status.HTTP_200_OK)

    def patch(self, request, pk):
        # post = self.get_object(pk)
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(instance=post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllPostsAPIView(APIView):
    """Все посты"""
    serializer_class = AllPostsSerializer
    pagination_class = Pagination

    @extend_schema(parameters=[OpenApiParameter('page', int), OpenApiParameter('title', str)])
    def get(self, request):
        paginator = Pagination()
        posts = Post.objects.all().select_related('author', 'type', 'group').order_by('-date_created')
        filtered_qs = posts.filter(title__icontains=request.GET.get('title', ''))
        paginated_qs = paginator.paginate_queryset(filtered_qs, request)
        return paginator.get_paginated_response(AllPostsSerializer(paginated_qs, many=True).data)


class CreatePostAPIView(APIView):
    serializer_class = CreatePostSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = Post.objects.create(title=request.data["title"])
        contents = request.data['post_content']
        for content in contents:
            PostContent.objects.create(
                post_id=data.id,
                text=content['text'],
                image=content['image'],
            )
        return Response(PostSerializer(data).data, status=status.HTTP_201_CREATED)
