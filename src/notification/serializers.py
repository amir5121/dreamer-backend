from rest_framework import serializers

from notification.models import UserNotification


class NotificationSerializer(serializers.ModelSerializer):
    identifier = serializers.CharField(source="notification.identifier")
    text = serializers.CharField(source="notification.text")
    title = serializers.CharField(source="notification.title")
    image = serializers.CharField(source="notification.image")

    class Meta:
        model = UserNotification
        fields = ["identifier", "text", "title", "created", "modified", "image"]
