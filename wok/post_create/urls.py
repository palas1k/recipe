from django.urls import path, include
from .views import *
from .views import AllPostsAPIView

urlpatterns = [
    path('', PostsList.as_view(template_name='foodrecipe/index.html'), name='home'),
    path('addpage/', CreatePost.as_view(template_name='foodrecipe/addpage.html'), name='add_post'),
    path('post/<int:pk>', PostView.as_view(), name='post-view'),
    path('posts/', AllPostsAPIView.as_view(), name='posts'),
    # path('profile/<int:pk>', ProfileDetail.as_view(), name='profile-view'),
]
