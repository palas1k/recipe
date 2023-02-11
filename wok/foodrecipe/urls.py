from django.urls import path, include
from .views import *

urlpatterns = [
    #path('posts/<int:pk>/', PostsList.as_view(), name = 'posts'),
    path('', PostsList.as_view(), name = 'posts'),
    path('addpage/', addpage, name = 'add_post')
]
