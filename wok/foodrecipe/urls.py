from django.urls import path, include
from .views import *

urlpatterns = [
    path('', PostsList.as_view(), name = 'home'),
    path('addpage/', CreatePost.as_view(), name = 'add_post'),
    #path('post/<int:pk>', ViewPost.as_view(), name = 'post-view'),

]
