import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel, SoftDeletableModel


class Post(TimeStampedModel, SoftDeletableModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    STATUS = Choices('personal', 'published', 'timeline')
    status = StatusField()
    text = ArrayField(models.TextField())
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        ordering = ['-created']

    @property
    def is_multi_text(self):
        return len(self.text) > 1
