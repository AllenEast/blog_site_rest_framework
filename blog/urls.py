from django.conf import settings
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.contrib import admin

from accounts.views import login_view, register_view, logout_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('comments/', include(("comments.urls", "comments"), namespace='comments')),

    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('posts/', include(("posts.urls", "posts"), namespace='posts')),
    path('api/users/', include('accounts.api.urls', namespace='users-api')),
    path('api/comments/', include('comments.api.urls', namespace='comments-api')),
    path('api/posts/', include('posts.api.urls', namespace='posts-api')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(("posts.urls", "posts"), namespace='posts-home')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
