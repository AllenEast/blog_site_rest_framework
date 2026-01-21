from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import CharField, ModelSerializer, EmailField
from django.db.models import Q

from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()

class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bu email allaqachon mavjud")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Bu username band")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get("username"),
            email=validated_data.get("email"),
            password=validated_data.get("password")
        )
        return user



class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(required=False, allow_blank=True)
    email = EmailField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "token"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        email = data.get("email", None)
        username = data.get("username", None)
        password = data.get("password")

        if not email and not username:
            raise ValidationError("Email yoki username kiritilishi shart")

        user = User.objects.filter(Q(email=email) | Q(username=username)).distinct()
        user = user.exclude(email__isnull=True).exclude(email__iexact="")
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("Email yoki username ro'yxatdan o'tmagan")

        if not user_obj.check_password(password):
            raise ValidationError("Parol noto'g'ri")

        # Token yaratish
        refresh = RefreshToken.for_user(user_obj)
        data["token"] = str(refresh.access_token)
        data['refresh'] = str(refresh)

        return data
