from django.contrib.auth import get_user_model
from rest_framework import serializers

from utils.serializers import SerializerFileMixin


class UserSelfSerializer(SerializerFileMixin, serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = [
            "id",
            "password",
            "groups",
            "user_permissions",
            "is_superuser",
            "is_staff",
            "is_active"
        ]

        read_only_fields = [
            "email",
            "username",
            "date_joined"
        ]
