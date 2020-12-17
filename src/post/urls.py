from django.urls import path, include
from rest_framework import routers

from post import views
from post.views import AnalyticsView

router = routers.DefaultRouter()
router.register(r"timeline", views.TimelineViewSet, basename="timeline")
router.register(r"dreams", views.DreamViewSet, basename="dreams")

urlpatterns = [
    path("", include(router.urls)),
    path("analytics/", AnalyticsView.as_view(), name="analytics-config"),
]
