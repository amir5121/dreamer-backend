from django.urls import path, include
from rest_framework import routers

from post import views

router = routers.DefaultRouter()
router.register(r"posts", views.PostViewSet, basename="posts")

urlpatterns = [
    path("", include(router.urls)),
]
