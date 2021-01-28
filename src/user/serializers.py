from django.contrib.auth import get_user_model
from rest_framework import serializers

from utils.serializers import SerializerFileMixin


class UserSelfSerializer(SerializerFileMixin, serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)
    gender_display = serializers.CharField(source="get_gender_display", read_only=True)

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
            "full_name",
            "birth_date",
            "gender",
            "gender_display",
        ]

        read_only_fields = [
            "email",
            "username",
            "date_joined",
            "gender_display",
            "full_name",
            "identifier",
        ]

    def to_representation(self, instance):
        result = super(UserSelfSerializer, self).to_representation(instance)
        if not bool(result['avatar']):
            result['avatar'] = f"https://loremflickr.com/g/320/320/girl/?lock={instance.id}"
        return result


class UserMinimalSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name")

    class Meta:
        model = get_user_model()
        fields = ["email", "username", "avatar", "full_name"]
        read_only_fields = fields.copy()

    def to_representation(self, instance):
        result = super(UserMinimalSerializer, self).to_representation(instance)
        if not bool(result['avatar']):
            result['avatar'] = f"https://loremflickr.com/g/320/320/girl/?lock={instance.id}"
        return result
