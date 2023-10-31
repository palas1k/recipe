from django.urls import path, include

from follow_likes.views import follow
# from userprofile.views import ProfileDetail

from .views import ProfileAPIView, MyProfileAPIView, SignUpView, ChangePasswordView

urlpatterns = [
    # path('<int:pk>/', ProfileDetail.as_view(), name='profile-view'),
    path('auth/', include('rest_framework.urls'), name='drf-auth'),
    path('<int:pk>/follow/', follow, name='follow'),
    path('<int:pk>/', ProfileAPIView.as_view(), name='profile'),
    path('me/', MyProfileAPIView.as_view(), name='my-profile'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('passupdate/', ChangePasswordView.as_view(), name='password-update')
]
