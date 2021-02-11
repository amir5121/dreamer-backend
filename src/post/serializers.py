from pydub import AudioSegment
from rest_framework import serializers
from rest_framework.fields import empty

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
    dream_clearance_display = serializers.CharField(
        source="get_dream_clearance_display"
    )
    voice_duration = serializers.SerializerMethodField()
    voice_wave = serializers.SerializerMethodField()

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
            "voice_duration",
            "voice_wave",
        ]

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance, data, **kwargs)
        self.audio_segment = None

    def get_audio_segment(self, instance):

        if self.audio_segment is None:
            self.audio_segment = AudioSegment.from_file(instance.voice.path)
        return self.audio_segment

    def get_voice_duration(self, instance: Dream):
        if instance.voice:
            return self.get_audio_segment(instance).duration_seconds * 1000
        else:
            return None

    def get_voice_wave(self, instance: Dream):
        if instance.voice:
            return (
                self.get_audio_segment(instance)
                .set_frame_rate(frame_rate=10)
                .get_array_of_samples()
            )
        else:
            return None


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
        instance = super(DreamWriteSerializer, self).create(
            validated_data=validated_data
        )
        for feeling in feelings:
            feeling.dream_id = instance.id
            Feeling.objects.create(dream_id=instance.id, **feeling)
        for element in elements:
            Element.objects.create(dream_id=instance.id, **element)
        return instance

    def update(self, instance, validated_data):
        feelings = validated_data.pop("feelings")
        elements = validated_data.pop("elements")
        instance = super(DreamWriteSerializer, self).update(
            instance=instance, validated_data=validated_data
        )
        if feelings:
            Feeling.objects.filter(dream_id=instance.id).delete()
            for feeling in feelings:
                feeling.dream_id = instance.id
                Feeling.objects.create(dream_id=instance.id, **feeling)
        if elements:
            Element.objects.filter(dream_id=instance.id).delete()
            for element in elements:
                Element.objects.create(dream_id=instance.id, **element)
        return instance
