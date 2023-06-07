from django.urls import path

from follow_likes_bms import views
from userprofile.views import ProfileDetail

urlpatterns = [
    path('<int:pk>/', ProfileDetail.as_view(), name='profile-view'),
    path('follow/<str:username>', views.follow_check, name='follow'),
]
