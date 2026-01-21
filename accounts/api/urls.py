app_name = 'comments-api'

from django.urls import path, re_path
from .views import UserCreateAPIView, UserLoginAPIView, LogoutAPIView

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='jwt-logout'),
    path('register/', UserCreateAPIView.as_view(), name='register'),

]
