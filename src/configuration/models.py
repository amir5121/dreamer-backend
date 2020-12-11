from django.db import models
from model_utils.models import TimeStampedModel

from utils.models import ModelVersionMixin


class DreamerConfiguration(ModelVersionMixin, TimeStampedModel):
    main_background = models.ImageField(upload_to="configurations/")
