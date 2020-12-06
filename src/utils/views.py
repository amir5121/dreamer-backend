import os
import pathlib
from uuid import uuid1

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import views, status
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.viewsets import GenericViewSet

from utils import rest_mixins
from utils.dreamer_response import DreamerResponse
from utils.rest_validation import DreamerValidationError
from utils.serializers import UploadSerializer


class DreamerGenericViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]
    read_serializer_class = None

    def get_user(self):
        return self.request.proxy_user or self.request.user

    def get_read_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_read_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        kwargs["context"].pop(
            "request", None
        )  # so serializer return relative image path
        return serializer_class(*args, **kwargs)

    def get_read_serializer_class(self):
        """
        Return the class to use for the read_serializer.
        Defaults to using `self.read_serializer_class`

        You may want to override this if you need to provide different
        response_serializations depending on the incoming request.

        """
        assert self.read_serializer_class is not None, (
                "'%s' should either include a `read_serializer_class` attribute, "
                "or override the `get_read_serializer_class()` method."
                % self.__class__.__name__
        )

        return self.read_serializer_class


class DreamerViewSet(
    rest_mixins.CreateModelMixin,
    rest_mixins.RetrieveModelMixin,
    rest_mixins.ListModelMixin,
    rest_mixins.UpdateModelMixin,
    rest_mixins.DestroyModelMixin,
    DreamerGenericViewSet,
):
    pass


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
