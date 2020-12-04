from django.urls import path, include
from rest_framework import routers

from configuration.views import InitialConfigView

router = routers.DefaultRouter()
# router.register(r"posts", InitialConfigView, basename="configurations")

urlpatterns = [
    path("", include(router.urls)),
    path("initial/", InitialConfigView.as_view(), name="initial-config"),
]
