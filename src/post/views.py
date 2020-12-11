from rest_framework.permissions import IsAuthenticated

from post.models import Post, Dream
from post.serializers import PostSerializer, DreamReadSerializer, DreamWriteSerializer
from utils import views, rest_mixins
from utils.views import DreamerGenericViewSet


class TimelineViewSet(
    rest_mixins.ListModelMixin,
    rest_mixins.RetrieveModelMixin,
    DreamerGenericViewSet,
):
    serializer_class = PostSerializer

    def get_queryset(self):
        posts_filters = dict()
        if "show_multi" in self.request.GET and self.action == "list":
            if self.request.GET["show_multi"].lower() == "true":
                posts_filters.update({"text__len__gt": 1})
            else:
                posts_filters.update({"text__len": 1})
        return Post.objects.filter(**posts_filters)


class DreamViewSet(views.DreamerViewSet):
    permission_classes = [IsAuthenticated]
    lookup_field = 'identifier'

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return DreamReadSerializer
        return DreamWriteSerializer

    def get_queryset(self):
        return Dream.objects.filter(user_id=self.request.user.id).prefetch_related("feelings")
