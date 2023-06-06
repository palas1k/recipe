from django.urls import path

from userprofile.views import ProfileDetail

urlpatterns = [
    path('<int:pk>/', ProfileDetail.as_view(), name='profile-view'),
    path('follow/<str:username>', )
]
