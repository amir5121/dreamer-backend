import uuid

from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel, SoftDeletableModel

from utils import constants


class Post(TimeStampedModel, SoftDeletableModel):
    publication_date = models.DateTimeField(auto_now_add=True)
    text = ArrayField(models.TextField())
    POST_TYPES = Choices("word_cloud", "timeline")

    post_type = StatusField(choices_name="POST_TYPES", default=POST_TYPES.timeline)

    class Meta:
        ordering = ["-created"]

    @property
    def is_multi_text(self):
        return len(self.text) > 1


def voice_upload_path(instance: "Dream", filename: str):
    return f'voices/{instance.user.identifier}/{filename}'


class Dream(TimeStampedModel, SoftDeletableModel):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    PUBLICATION_STATUS = Choices(
        "personal",
        "published",
    )
    publication_status = StatusField(choices_name="PUBLICATION_STATUS")
    dream_clearance = models.PositiveSmallIntegerField(
        choices=constants.CLEARANCE, default=constants.NORMAL
    )
    text = models.TextField(null=True, blank=True)
    title = models.TextField()
    dream_date = models.DateTimeField()
    voice = models.FileField(upload_to=voice_upload_path, blank=True, null=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"{self.user} {self.title}"


class FeelingDetail(SoftDeletableModel):
    parent_type = models.CharField(max_length=64, choices=constants.MAIN_FEELINGS)
    detailed_type = models.CharField(
        max_length=64, choices=constants.FEELINGS, null=True, blank=True
    )
    description = models.TextField()
    color = ColorField(default="#1F182E")

    @staticmethod
    def main_feelings():
        return FeelingDetail.objects.filter(detailed_type__isnull=True)

    @staticmethod
    def detailed_feelings():
        return FeelingDetail.objects.filter(detailed_type__isnull=False)

    def clean(self):
        if self.detailed_type and self.parent_type not in self.detailed_type:
            raise ValidationError("Can't have mixed feeling..")
        if (
                self.detailed_type is None
                and self.__class__.objects.filter(
            parent_type=self.parent_type, detailed_type__isnull=True
        )
                .exclude(id=self.id)
                .count()
                > 1
        ):
            raise ValidationError(f"Multiple parent for type {self.parent_type}")

    def __str__(self):
        return f"{self.detailed_type or self.parent_type}"


class Feeling(models.Model):
    dream = models.ForeignKey(Dream, on_delete=models.CASCADE, related_name="feelings")
    rate = models.PositiveSmallIntegerField(
        default=0,
        validators=[MaxValueValidator(10), MinValueValidator(0)],
    )
    feeling = models.ForeignKey(FeelingDetail, on_delete=models.PROTECT)

    def clean(self):
        if self.feeling.detailed_type is None:
            raise ValidationError(f"Must be a detailed feeling")


class Element(models.Model):
    dream = models.ForeignKey(Dream, on_delete=models.CASCADE, related_name="elements")
    elements = ArrayField(models.TextField())
    type = models.CharField(max_length=64, choices=constants.ELEMENTS)
