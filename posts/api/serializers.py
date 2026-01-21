from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField
from posts.models import Post
from markdown_deux import markdown
from comments.api.serializers import CommentDetailSerializer, CommentSerializer
from comments.models import Comment
from accounts.api.serializers import UserDetailSerializer


class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'publish',]

post_detail_url = HyperlinkedIdentityField(
        view_name='posts-api:detail',
        lookup_field='slug',

        )

class PostDetailSerializer(ModelSerializer):
    url = post_detail_url
    user = UserDetailSerializer(read_only=True)
    image = SerializerMethodField()
    markdown = SerializerMethodField()
    comments = SerializerMethodField()
    class Meta:
        model = Post
        fields = ['url', 'id', 'user', 'title', 'slug', 'content', 'publish', 'image', 'markdown', 'comments']

    def get_markdown(self, obj):
        return markdown(obj.content)


    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    def get_comments(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(c_qs, many=True).data
        return comments


class PostListSerializer(ModelSerializer):
    url = post_detail_url
    UserDetailSerializer(read_only=True)
    # url = HyperlinkedIdentityField(
    #     view_name='posts-api:detail',
    #     lookup_field='slug'
    #     )
    # delete_url = HyperlinkedIdentityField(
    #     view_name='posts-api:delete',
    #     lookup_field='slug'
    # )


    class Meta:
        model = Post
        fields = ['url', 'user', 'title', 'content', 'publish']

