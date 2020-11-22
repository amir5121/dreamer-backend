from django.urls import path

from utils.views import FileUploadView, InitialConfigView

urlpatterns = [
    path("configurations/", InitialConfigView.as_view(), name="initial-config"),
    path("upload/", FileUploadView.as_view(), name="uploader"),
]
