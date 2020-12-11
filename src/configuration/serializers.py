from rest_framework import serializers

from configuration.models import DreamerConfiguration
from post.models import FeelingDetail
from post.serializers import FeelingDetailSerializer
from user.serializers import UserSelfSerializer
from utils import constants


class ConfigurationsSerializer(serializers.ModelSerializer):
    self = serializers.SerializerMethodField()
    feelings = serializers.SerializerMethodField()
    main_feelings = serializers.SerializerMethodField()
    clearance_choices = serializers.SerializerMethodField()

    class Meta:
        model = DreamerConfiguration
        fields = "__all__"

    def get_self(self, _):
        request_user = self.context["request"].user
        if request_user.is_authenticated:
            return UserSelfSerializer(instance=request_user, context=self.context).data
        return None

    @staticmethod
    def get_clearance_choices(_):
        result = []
        for value, label in dict(constants.CLEARANCE).items():
            result.append(
                {
                    "value": value,
                    "label": label,
                }
            )

        return result

    @staticmethod
    def get_feelings(_):
        return FeelingDetailSerializer(
            many=True,
            instance=FeelingDetail.objects.filter(detailed_type__isnull=False),
        ).data

    @staticmethod
    def get_main_feelings(_):
        return FeelingDetailSerializer(
            many=True, instance=FeelingDetail.objects.filter(detailed_type__isnull=True)
        ).data
