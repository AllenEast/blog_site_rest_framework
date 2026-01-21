from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView, \
    RetrieveUpdateAPIView
from comments.models import Comment
from .serializers import CommentDetailSerializer, CommentListSerializer, create_comment_serializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, \
    IsAuthenticatedOrReadOnly
from posts.api.permissions import IsOwnerOrReader
from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    # serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        model_type = self.request.data.get('type', 'post')
        slug = self.request.data.get('slug')
        parent_id = self.request.data.get('parent_id', None)
        return create_comment_serializer(
            model_type=model_type,
            slug=slug,
            parent_id=parent_id,
            user=self.request.user,
        )



class CommentDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'


    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class CommentListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['content', 'user__first_name', 'user__last_name']
    pagination_class = PostPageNumberPagination

    def get_queryset(self):
        queryset_list = Comment.objects.filter(object_id__gte=0)
        query = self.request.GET.get("q")

        if query:
            queryset_list = queryset_list.filter(
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()

        return queryset_list

