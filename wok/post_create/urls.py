from django.urls import path, include
from .views import *
from userprofile.views import *

urlpatterns = [
    path('', PostsList.as_view(), name='home'),
    path('addpage/', CreatePost.as_view(template_name='foodrecipe/addpage.html'), name='add_post'),
    path('post/<int:pk>', PostView.as_view(), name='post-view'),
    # path('profile/<int:pk>', ProfileDetail.as_view(), name='profile-view'),
]
