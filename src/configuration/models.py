from django.db import models
from model_utils.models import TimeStampedModel

from utils import constants
from utils.models import ModelVersionMixin


class DreamerConfiguration(ModelVersionMixin, TimeStampedModel):
    main_background = models.ImageField(upload_to="configurations/")


class FeelingDetail(models.Model):
    type = models.CharField(max_length=64, choices=constants.FEELINGS)
    description = models.TextField()
