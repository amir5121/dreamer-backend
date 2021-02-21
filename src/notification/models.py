import uuid

from django.contrib.auth import get_user_model
from django.db import models
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel
from versatileimagefield.fields import VersatileImageField


class Notification(TimeStampedModel):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    text = models.TextField()
    title = models.TextField()
    image = VersatileImageField(upload_to='notifications/', blank=True, null=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["-created"]


class UserNotification(TimeStampedModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)

    NOTIFICATION_CHOICES = Choices("created", "send", "read")
    state = StatusField(
        choices_name="NOTIFICATION_CHOICES", default=NOTIFICATION_CHOICES.created
    )

    class Meta:
        ordering = ["-created"]
