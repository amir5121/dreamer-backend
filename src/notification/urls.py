from django.urls import path, include
from rest_framework import routers

from notification import views

router = routers.DefaultRouter()
router.register(r"notifications", views.NotificationViewSet, basename="notifications")

urlpatterns = [
    path("", include(router.urls)),
]
