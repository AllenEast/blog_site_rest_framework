app_name = 'comments-api'

from django.urls import path, re_path
from .views import CommentListAPIView, CommentDetailAPIView, CommentCreateAPIView

urlpatterns = [
    path('list/', CommentListAPIView.as_view(), name='list'),
    path('create/', CommentCreateAPIView.as_view(), name='create'),
    path('<int:pk>/', CommentDetailAPIView.as_view(), name='detail'),
]
