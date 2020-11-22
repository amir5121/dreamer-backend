import os
import pathlib
from uuid import uuid1

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import views, status
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from user.serializers import UserSelfSerializer
from utils.dreamer_response import DreamerResponse
from utils.rest_validation import DreamerValidationError
from utils.serializers import UploadSerializer


class InitialConfigView(views.APIView):

    def get(self, request, *args, **kwargs):
        result = {
            "self": None
        }
        if request.user.is_authenticated:
            result.update(
                {
                    "self": UserSelfSerializer(instance=request.user).data

                }
            )
        return DreamerResponse(data=result).toJSONResponse()


class FileUploadView(views.APIView):
    parser_classes = (MultiPartParser, FileUploadParser,)
    permission_classes = [IsAuthenticated]
    MAX_UPLOAD_SIZE = 10485760
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "file_upload_throttle"

    def put(self, request, *args, **kwargs):
        serializer = UploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data["file"]

        if file.size > self.MAX_UPLOAD_SIZE:
            raise DreamerValidationError(
                message_code="max_upload_size",
                message=_("File is too large"),
            )

        else:
            ext = file.name.split(".")[-1]
            file_path = os.path.join('temp', f"{uuid1()}.{ext}")

            directory_path = os.path.join(settings.MEDIA_ROOT, file_path[0:file_path.rfind('/')])
            pathlib.Path(directory_path).mkdir(parents=True, exist_ok=True)

            with open(os.path.join(settings.MEDIA_ROOT, file_path), "wb+") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            return DreamerResponse(
                data={"file_path": settings.MEDIA_URL + file_path},
                message=_("successfully uploaded"),
                code=status.HTTP_201_CREATED
            ).toJSONResponse()

    def post(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)
