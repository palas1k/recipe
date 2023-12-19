from django.urls import path, include

from .views import CommentsAPIView, CommentsRetrieveAPIView

urlpatterns = [
    path('post/<int:pk>/comment/', CommentsAPIView.as_view(), name='create-comment'),
    path('comments/<int:comment_pk>/', CommentsRetrieveAPIView.as_view(), name='retrieve-comment'),
]
