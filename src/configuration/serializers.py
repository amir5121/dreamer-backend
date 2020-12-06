import os

from rest_framework import serializers
from rest_framework.fields import FileField

from configuration.models import DreamerConfiguration
from post.models import Post
from user.serializers import UserMinimalSerializer, UserSelfSerializer
from utils.functions import get_uploaded_file


class ConfigurationsSerializer(serializers.ModelSerializer):
    self = serializers.SerializerMethodField()

    class Meta:
        model = DreamerConfiguration
        fields = '__all__'

    def get_self(self, _):
        request_user = self.context["request"].user
        if request_user.is_authenticated:
            return UserSelfSerializer(instance=request_user, context=self.context).data
        return None
