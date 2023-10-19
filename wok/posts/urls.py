from django.urls import path, include

from comments.views import CommentsAPIView
from .views import *
from .views import AllPostsAPIView, PostRetrieveAPIView, CreatePostAPIView

urlpatterns = [
    # path('', PostsList.as_view(template_name='foodrecipe/index.html'), name='home'),
    # path('addpage/', CreatePost.as_view(template_name='foodrecipe/addpage.html'), name='add_post'),
    # path('post/<int:pk>', PostView.as_view(), name='post-view'),
    path('posts/', AllPostsAPIView.as_view(), name='posts'),
    path('post/<int:pk>/', PostRetrieveAPIView.as_view(), name='post-detail'),
    path('post/<int:pk>/comment/', CommentsAPIView.as_view(), name='comment'),
    path('post/create/', CreatePostAPIView.as_view(), name='post-create'),
    # path('profile/<int:pk>', ProfileDetail.as_view(), name='profile-view'),
]
