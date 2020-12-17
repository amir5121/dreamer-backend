import os
from uuid import uuid1

from django.conf import settings
from django.core.files import File


def directory_path(instance, filename):
    ext = filename.split(".")[-1]
    return "images/{}/{}.{}".format(instance._meta.app_label, str(uuid1()), ext)


def conversation_path(instance, filename):
    ext = filename.split(".")[-1]
    return f"conversations/{instance.conversation.identifier}/{str(uuid1())}.{ext}"


def get_uploaded_file(file_path):
    file_path = os.path.join(settings.BASE_DIR, *file_path.split("/"))
    if not file_path.startswith(settings.MEDIA_ROOT):
        raise ValueError("Access denied.")
    file = open(file_path, "rb")
    return File(file, name=file_path.split("/")[-1])


def get_request_host(request):
    return request.scheme + "://" + request.get_host()
