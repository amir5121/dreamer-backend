from datetime import timedelta

from django.db.models import Sum, Avg
from django.db.models.functions import TruncDay, TruncMonth
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from post.helpers.word_cloud_helpers import get_word_cloud_image
from post.models import Post, Dream, Feeling, FeelingDetail
from post.serializers import PostSerializer, DreamReadSerializer, DreamWriteSerializer
from utils import views, rest_mixins
from utils.dreamer_response import DreamerResponse
from utils.functions import get_request_host
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.feelings = list()
        self.request = None
        self.duration = 7
        self.dreams = None
        self.dreams_count = 0

    def get(self, request, *args, **kwargs):
        self.request = request
        self.duration = int(request.GET.get("duration", 7))
        self.dreams = Dream.objects.filter(
            created__gte=timezone.now() - timedelta(days=self.duration),
            user_id=request.user.id,
        ).prefetch_related("elements")
        self.dreams_count = self.dreams.count()
        self.set_feelings_sum()
        trunc_func = TruncDay if self.duration < 128 else TruncMonth
        return DreamerResponse(
            data={
                "main_quote": self.get_main_quote(),
                "word_cloud": self.get_word_cloud(),
                "feelings": self.feelings,
                "dreams_count": self.dreams_count,
                "clearances": self.dreams.annotate(day=trunc_func("created"))
                .values("day")
                .order_by("day")
                .annotate(average=Avg("dream_clearance")),
            }
        ).toJSONResponse()

    @staticmethod
    def get_main_quote():
        try:
            return (
                Post.objects.filter(post_type=Post.POST_TYPES.word_cloud)
                .order_by("modified")
                .last()
                .text[0]
            )
        except AttributeError:
            return ""

    def get_word_cloud(self):
        return (
            get_request_host(self.request)
            + "/"
            + get_word_cloud_image(
                dreams=self.dreams, duration=self.duration, user_id=self.request.user.id
            )
        )

    def set_feelings_sum(self):
        feeling_grouped = list(
            Feeling.objects.filter(
                dream__user_id=self.request.user.id,
                dream__created__gte=timezone.now() - timedelta(days=self.duration),
            )
            .values("feeling__parent_type")
            .annotate(rates_sum=Sum("rate"))
        )
        total = sum([i["rates_sum"] for i in feeling_grouped])
        for feeling in FeelingDetail.main_feelings():
            if total < 1:
                self.feelings.append({"name": feeling.parent_type, "value": 0})
            else:
                feeling_sum = list(
                    filter(
                        lambda x: x["feeling__parent_type"] == feeling.parent_type,
                        feeling_grouped,
                    )
                )
                if len(feeling_sum) > 0:
                    feeling_sum = feeling_sum[0]["rates_sum"]
                else:
                    feeling_sum = 0
                self.feelings.append(
                    {
                        "label": feeling.parent_type,
                        "value": feeling_sum / total,
                        "color": feeling.color,
                    }
                )
