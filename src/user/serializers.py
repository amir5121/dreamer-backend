from django.contrib.auth import get_user_model
from rest_framework import serializers

from utils.serializers import SerializerFileMixin


class UserSelfSerializer(SerializerFileMixin, serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name")

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "first_name",
            "last_name",
            "date_joined",
            "email",
            "identifier",
            "avatar",
            "avatar_image",
            "full_name",
        ]

        read_only_fields = [
            "email",
            "username",
            "date_joined"
        ]


class UserMinimalSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name")

    class Meta:
        model = get_user_model()
        fields = ["email", "username", "avatar_image", "full_name"]
        read_only_fields = fields.copy()
