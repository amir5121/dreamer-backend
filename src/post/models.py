import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel, SoftDeletableModel

from utils import constants


class Post(TimeStampedModel, SoftDeletableModel):
    publication_date = models.DateTimeField(auto_now_add=True)
    text = ArrayField(models.TextField())

    class Meta:
        ordering = ["-created"]

    @property
    def is_multi_text(self):
        return len(self.text) > 1


class Dream(TimeStampedModel, SoftDeletableModel):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    PUBLICATION_STATUS = Choices(
        "personal",
        "published",
    )
    publication_status = StatusField(choices_name="PUBLICATION_STATUS")
    DREAM_CLEARANCE = Choices(
        "cloudy",
        "normal",
        "clear",
        "super_clear",
    )
    dream_clearance = StatusField(choices_name="DREAM_CLEARANCE")
    text = models.TextField()
    title = models.TextField()
    dream_date = models.DateTimeField()
    voice = models.FileField(blank=True, null=True)

    class Meta:
        ordering = ["-created"]


class Feeling(models.Model):
    dream = models.ForeignKey(Dream, on_delete=models.CASCADE, related_name='feelings')
    rate = models.PositiveSmallIntegerField(default=0)
    type = models.CharField(max_length=64, choices=constants.FEELINGS)


class Element(models.Model):
    dream = models.ForeignKey(Dream, on_delete=models.CASCADE, related_name='elements')
    elements = ArrayField(models.TextField())
    type = models.CharField(max_length=64, choices=constants.ELEMENTS)
