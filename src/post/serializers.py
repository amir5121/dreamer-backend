from rest_framework import serializers

from post.models import Post, Dream, Element, Feeling
from user.serializers import UserMinimalSerializer


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["text", "is_multi_text", "created"]


class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = [
            "elements",
            "type",
        ]


class FeelingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feeling
        fields = [
            "rate",
            "type",
        ]


class DreamSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer()
    elements = ElementSerializer(many=True)
    feelings = FeelingSerializer(many=True)

    class Meta:
        model = Dream
        fields = [
            "text",
            "created",
            "modified",
            "user",
            "identifier",
            "publication_status",
            "title",
            "dream_date",
            "voice",
            "feelings",
            "elements",
        ]
