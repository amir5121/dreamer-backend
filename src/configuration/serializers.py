from rest_framework import serializers

from configuration.models import DreamerConfiguration
from post.models import FeelingDetail
from post.serializers import FeelingDetailSerializer
from user.serializers import UserSelfSerializer
from utils import constants
from utils.functions import convert_to_label_value


class ConfigurationsSerializer(serializers.ModelSerializer):
    self = serializers.SerializerMethodField()
    clearance_choices = serializers.SerializerMethodField()
    gender_choices = serializers.SerializerMethodField()
    feelings = serializers.SerializerMethodField()
    main_feelings = serializers.SerializerMethodField()

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
        return convert_to_label_value(constants.CLEARANCE)

    @staticmethod
    def get_feelings(_):
        return FeelingDetailSerializer(
            many=True,
            instance=FeelingDetail.detailed_feelings()
        ).data

    @staticmethod
    def get_main_feelings(_):
        return FeelingDetailSerializer(
            many=True, instance=FeelingDetail.main_feelings()
        ).data

    @staticmethod
    def get_gender_choices(_):
        return convert_to_label_value(constants.GENDERS)
