from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel, UUIDModel


class BaseModelClass(TimeStampedModel, SoftDeletableModel, UUIDModel):
    class Meta:
        abstract = True
