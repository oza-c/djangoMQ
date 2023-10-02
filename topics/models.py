from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class unitsModel(models.Model):
    unit_name = models.CharField(name="unit_name", max_length=50)
    unit_char = models.CharField(name="unit_char", max_length=20)

class topicModel(models.Model):
    topic_name = models.CharField(name="topic_name", max_length=50)
    topic_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=""
    )
    topic_unit = models.ForeignKey(
        unitsModel,
        on_delete=models.CASCADE,
        default=""
    )



