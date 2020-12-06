from django.urls import path, include
from rest_framework import routers

from post import views

router = routers.DefaultRouter()
router.register(r"timeline", views.TimelineViewSet, basename="timeline")
router.register(r"dreams", views.DreamViewSet, basename="dreams")

urlpatterns = [
    path("", include(router.urls)),
]
