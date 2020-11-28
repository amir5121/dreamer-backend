import os

from rest_framework import serializers
from rest_framework.fields import FileField

from post.models import Post
from user.serializers import UserMinimalSerializer
from utils.functions import get_uploaded_file


class PostSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer()

    class Meta:
        model = Post
        exclude = ['id', 'is_removed']
