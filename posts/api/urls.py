from django.urls import path
from .views import (
    PostCreateAPIView,
    PostListAPIView,
    PostDetailAPIView,
    PostUpdateAPIView,
    PostDeleteAPIView,
)

app_name = "posts_api"

urlpatterns = [
    path('posts_list/', PostListAPIView.as_view(), name='post-list'),
    path('create/', PostCreateAPIView.as_view(), name='create'),
    path('<slug:slug>/', PostDetailAPIView.as_view(), name='detail'),
    path('<slug:slug>/edit/', PostUpdateAPIView.as_view(), name='update'),
    path('<slug:slug>/delete/', PostDeleteAPIView.as_view(), name='delete'),
]
