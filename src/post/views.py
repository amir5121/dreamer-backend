from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from post.helpers.word_cloud_helpers import get_word_cloud_image
from post.models import Post, Dream
from post.serializers import PostSerializer, DreamReadSerializer, DreamWriteSerializer
from utils import views, rest_mixins
from utils.dreamer_response import DreamerResponse
from utils.views import DreamerGenericViewSet


class TimelineViewSet(
    rest_mixins.ListModelMixin,
    rest_mixins.RetrieveModelMixin,
    DreamerGenericViewSet,
):
    serializer_class = PostSerializer

    def get_queryset(self):
        posts_filters = {"post_type": Post.POST_TYPES.timeline}
        if "show_multi" in self.request.GET and self.action == "list":
            if self.request.GET["show_multi"].lower() == "true":
                posts_filters.update({"text__len__gt": 1})
            else:
                posts_filters.update({"text__len": 1})
        return Post.objects.filter(**posts_filters)


class DreamViewSet(views.DreamerViewSet):
    permission_classes = [IsAuthenticated]
    lookup_field = "identifier"

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return DreamReadSerializer
        return DreamWriteSerializer

    def get_queryset(self):
        return Dream.objects.filter(user_id=self.request.user.id).prefetch_related(
            "feelings"
        )


class AnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, *args, **kwargs):
        duration = int(request.GET.get("duration", 7))
        return DreamerResponse(
            data={
                "main_quote": Post.objects.filter(post_type=Post.POST_TYPES.word_cloud)
                .order_by("modified")
                .last(),
                "word_cloud": get_word_cloud_image(duration, request.user.id),
            }
        ).toJSONResponse()
