from django import forms

from mqtt.models import brokerConnectionSettingsModel
from .models import topicModel


class TopicForm(forms.ModelForm):
    class Meta:
        model = topicModel
        fields=['topic_name']
        labels={'topic_name' : "" }

class MqttBrokerForm(forms.ModelForm):
    class Meta:
        model = brokerConnectionSettingsModel
        fields=['broker_name', 'broker_ip', 'broker_username', 'broker_password', 'broker_port']