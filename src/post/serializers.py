from rest_framework import serializers

from post.models import Post, Dream, Element, Feeling, FeelingDetail
from user.serializers import UserMinimalSerializer
from utils.serializers import SerializerFileMixin


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "text", "is_multi_text", "created"]


class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = [
            "elements",
            "type",
        ]


class FeelingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeelingDetail
        fields = ["description", "detailed_type", "parent_type"]


class FeelingSerializer(serializers.ModelSerializer):
    feeling = serializers.SlugRelatedField(
        slug_field="detailed_type", queryset=FeelingDetail.objects.all()
    )
    feeling_parent = serializers.CharField(source="feeling.parent_type", read_only=True)

    class Meta:
        model = Feeling
        fields = [
            "feeling",
            "feeling_parent",
            "rate",
        ]


class DreamReadSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer()
    elements = ElementSerializer(many=True)
    feelings = FeelingSerializer(many=True)
    dream_clearance_display = serializers.CharField(source='get_dream_clearance_display')

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
            "dream_clearance",
            "dream_clearance_display",
        ]


class DreamWriteSerializer(SerializerFileMixin, serializers.ModelSerializer):
    elements = ElementSerializer(many=True)
    feelings = FeelingSerializer(many=True)

    class Meta:
        model = Dream
        fields = [
            "text",
            "user",
            "title",
            "dream_date",
            "voice",
            "feelings",
            "dream_clearance",
            "elements",
        ]

    def to_internal_value(self, data):
        data["user"] = self.context["request"].user.id
        return super(DreamWriteSerializer, self).to_internal_value(data)

    def create(self, validated_data):
        feelings = validated_data.pop("feelings")
        elements = validated_data.pop("elements")
        instance = super(DreamWriteSerializer, self).create(validated_data=validated_data)
        for feeling in feelings:
            feeling.dream_id = instance.id
            Feeling.objects.create(dream_id=instance.id, **feeling)
        for element in elements:
            Element.objects.create(dream_id=instance.id, **element)
        return instance
