
import paho.mqtt.client as mqtt
from topics.models import topicModel
from .models import brokerConnectionSettingsModel, mqttTopicData
from django.apps import apps
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

TopicModel = apps.get_model('topics', 'TopicModel')
active_clients = {}
subscribed_topics = {}

def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    try:
        topic = topicModel.objects.get(topic_name=message.topic)
        mqttTopicData.objects.create(
            mqtt_topic=topic,
            mqtt_timestamp=timezone.now(),
            mqtt_payload=payload
        )

        user_id = f"user_{topic.topic_user.id}"
        channel_layer = get_channel_layer()
        data_to_send = {"data": {"topic_name": topic.topic_name, "payload": payload, "timestamp": str(timezone.now())}}
        async_to_sync(channel_layer.group_send)(
            user_id, 
            {"type": "send_data", "data": data_to_send}  # Nachricht an den WebSocket-Consumer senden
        )
    except topicModel.DoesNotExist:
        client.unsubscribe(message.topic)


def onUserChangeMqttSettings(user_id):
    disconnect_client(user_id)
    connect_client(user_id)

def connect_clients():
    for userSettings in brokerConnectionSettingsModel.objects.all():
        connect_client(userSettings.broker_user)
        
def connect_client(user_id):
    client = connect_to_broker(user_id)
    client.on_message = on_message
    client.loop_start()

    topics = TopicModel.objects.filter(topic_user=user_id)
    for topic in topics:
        subscribe_topic(user_id,topic.topic_name)

def connect_to_broker(user_id):
    user_settings = brokerConnectionSettingsModel.objects.get(broker_user_id=user_id)
    
    client = mqtt.Client()
    active_clients[user_id] = client
    client.username_pw_set(user_settings.broker_username, user_settings.broker_password)
    client.tls_set()
    client.connect(user_settings.broker_ip, user_settings.broker_port)
    return client

def disconnect_client(user_id):
    if user_id in active_clients:
        client = active_clients.pop(user_id)
        client.disconnect()

def subscribe_topic(user_id, topic_name):
    if user_id not in subscribed_topics:
        subscribed_topics[user_id] = []

    subscribed_topics[user_id].append(topic_name)
    client = active_clients.get(user_id)
    if client:
        client.subscribe(topic_name)

def unsubscribe_topic(user_id, topic_name):
    if user_id in subscribed_topics:
        if topic_name in subscribed_topics[user_id]:
            subscribed_topics[user_id].remove(topic_name)
            client = active_clients.get(user_id)
            if client:
                client.unsubscribe(topic_name)

