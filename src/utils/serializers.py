import os

from rest_framework import serializers
from rest_framework.fields import FileField

from utils.functions import get_uploaded_file


class UploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)
    type = serializers.CharField(allow_blank=True, allow_null=True, required=False)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class SerializerFileMixin(object):
    to_delete = []

    def to_internal_value(self, data):
        for key, field in self.fields.items():
            if isinstance(field, FileField) and key in data and data[key]:
                data[key] = get_uploaded_file(data[key])
                self.to_delete.append(data[key].file.name)

        return super(SerializerFileMixin, self).to_internal_value(data)

    def save(self, **kwargs):
        res = super(SerializerFileMixin, self).save(**kwargs)
        for file in self.to_delete:
            try:
                os.remove(file)
            except FileNotFoundError:
                pass
        return res
