from django.urls import path, include
from rest_framework import routers

from user import views

router = routers.DefaultRouter()
# router.register(r"self", views.SelfViewSet, basename="self")

urlpatterns = [
    path("", include(router.urls)),
]
