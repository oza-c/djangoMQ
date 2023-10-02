from django.db import models
from django.conf import settings

from topics.models import topicModel

class brokerConnectionSettingsModel(models.Model):
    broker_name = models.CharField(name="broker_name", max_length=50, default="")
    broker_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=""
    )
    broker_ip = models.CharField(name="broker_ip", max_length=50)
    broker_port = models.BigIntegerField(name="broker_port", default=1883)
    broker_username = models.CharField(name="broker_username", max_length=50)
    broker_password = models.CharField(name="broker_password", max_length=50)


class mqttTopicData(models.Model):
    mqtt_topic = models.ForeignKey(
        topicModel,
        on_delete=models.CASCADE,
        default=""
    )
    mqtt_timestamp = models.CharField(name="mqtt_timestamp", max_length=100)
    mqtt_payload = models.CharField(name="mqtt_payload", max_length=50)
