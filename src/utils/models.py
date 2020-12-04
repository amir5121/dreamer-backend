from django.db import models
from model_utils import Choices
from model_utils.fields import StatusField


class ModelVersionMixin(models.Model):
    VERSION = Choices('v1', 'v2', 'v3')
    version = StatusField(choices_name='VERSION')

    class Meta:
        abstract = True
