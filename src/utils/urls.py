from django.urls import path

from utils.views import FileUploadView

urlpatterns = [
    path("upload/", FileUploadView.as_view(), name="uploader"),
]
