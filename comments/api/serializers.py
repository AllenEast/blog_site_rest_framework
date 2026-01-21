from rest_framework.relations import HyperlinkedRelatedField
from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField, \
    HyperlinkedModelSerializer
from posts.models import Post
from comments.models import Comment
from django.contrib.auth import get_user_model
from accounts.api.serializers import UserDetailSerializer
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment
User = get_user_model()


def create_comment_serializer(model_type='post', slug=None, parent_id=None, user=None):
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model = Comment
            fields = [
                "id",
                "content",
                "timestamp"
            ]
        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.slug = slug
            self.parent_obj = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)
        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)
            print('8'*10, model_qs)
            if not model_qs.exists() or (model_qs.count() != 1):
                raise serializers.ValidationError("This field is required.")
            Somemodel = model_qs.first().model_class()
            obj_qs = Somemodel.objects.filter(slug=self.slug)
            if not obj_qs.exists() or (obj_qs.count() != 1):
                raise serializers.ValidationError("This field is required for this model.")
            return data

        def create(self, validated_data):
            content = validated_data.get('content')
            if user:
                main_user = user
            else:
                main_user = User.objects.all().first()
            model_type = self.model_type
            slug = self.slug
            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(
                model_type, slug, content, main_user,
                parent_obj=parent_obj
                )
            return comment

    return CommentCreateSerializer

class CommentSerializer(ModelSerializer):
    reply_count = SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            "id",
            "content_type",
            "object_id",
            "parent",
            "content",
            "timestamp",
            "reply_count",
        ]

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

class CommentListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='comments-api:detail')
    reply_count = SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            "url",
            "id",
            "content",
            "timestamp",
            "reply_count",
        ]

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentChildSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'timestamp'
        ]

class CommentDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    reply_count = SerializerMethodField()
    content_object_url = SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "content",
            "timestamp",
            "replies",
            "reply_count",
            "content_object_url",
        ]
        read_only_fields = [
            # 'content_type',
            # 'object_id',
            'reply_count',
            'replies'
        ]

    def get_content_object_url(self, obj):
        try:
            return obj.content_object.get_absolute_url()
        except:
            return None
    def get_replies(self, obj):
        qs = Comment.objects.filter(parent=obj)
        return CommentDetailSerializer(qs, many=True).data

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


