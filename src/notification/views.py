from notification.models import UserNotification
from notification.serializers import NotificationSerializer
from utils import rest_mixins
from utils.views import DreamerGenericViewSet


class NotificationViewSet(
    rest_mixins.ListModelMixin,
    rest_mixins.RetrieveModelMixin,
    DreamerGenericViewSet,
):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return UserNotification.objects.filter(user_id=self.request.user.id)
