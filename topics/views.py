from json import dump
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core import serializers

from mqtt.models import brokerConnectionSettingsModel
from mqtt.models import mqttTopicData
from mqtt.mqtt_helper import unsubscribe_topic,subscribe_topic, onUserChangeMqttSettings
from .forms import MqttBrokerForm, TopicForm
from .models import topicModel, unitsModel

def index(request):
    if request.user.is_authenticated:
        return dashboard(request)
    return HttpResponseRedirect(reverse('web:login'))


def topic_loeschen(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            topic_to_delete = topicModel.objects.get(id=id)
            topic_to_delete.delete()
            unsubscribe_topic(request.user, topic_to_delete.topic_name)
    return HttpResponseRedirect(reverse('web:login'))

def topic_hinzufuegen(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = TopicForm(request.POST)
            form.instance.topic_user = request.user
            form.instance.topic_unit = unitsModel.objects.get(unit_name = request.POST["topic_unit"])
            if form.is_valid():
                form.save()
                subscribe_topic(request.user, form.instance.topic_name)
                return redirect("topics:index")
        else:
            form = TopicForm()
        return dashboard(request)
    return HttpResponseRedirect(reverse('web:login'))


def dashboard(request):
    if request.user.is_authenticated:
        form = TopicForm()
        topics = topicModel.objects.filter(topic_user=request.user)
        units = unitsModel.objects.all()
        chart_data = {}
        for topic in topics:
            topic_data = mqttTopicData.objects.filter(mqtt_topic=topic)
            labels = []
            data = []

            for data_point in topic_data:
                labels.append(data_point.mqtt_timestamp)
                data.append(float(data_point.mqtt_payload))

            chart_data[topic.topic_name] = {
                'labels': labels,
                'data': data,
            }
        
        return render(request, 'topics/dashboard.html', {'topics': topics, 'form': form, 'units': units, 'chart_data': chart_data})

def settings_change(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            setobj = brokerConnectionSettingsModel.objects.filter(broker_user=request.user).first()
            if setobj:
                form = MqttBrokerForm(request.POST, instance=setobj)
            else:
                form = MqttBrokerForm(request.POST)
            form.instance.broker_user = request.user
            if form.is_valid():
                form.save()
                onUserChangeMqttSettings(request.user)
            return redirect("topics:settings")
    else:
        return HttpResponseRedirect(reverse('web:login'))


def settings(request):
    if request.user.is_authenticated:
            form = MqttBrokerForm(instance=brokerConnectionSettingsModel.objects.filter(broker_user=request.user).first())
            return render(request, "topics/settings.html", {"form" : form} )
    return HttpResponseRedirect(reverse('web:login'))


def detailTopic(request, topicname):
    if request.user.is_authenticated:
        topic = get_object_or_404(topicModel, topic_name=topicname)

        if topic.topic_user == request.user:
            topic_data = mqttTopicData.objects.filter(mqtt_topic=topic)
            chart_data = {}
            labels = []
            data = []
            for data_point in topic_data:
                labels.append(data_point.mqtt_timestamp)
                data.append(float(data_point.mqtt_payload))

                chart_data[topic.topic_name] = {
                    'labels': labels,
                    'data': data,
                }
            return render(request, "topics/detail.html", {'topic_data': topic_data, 'chart_data': chart_data, 'topic': topic})
        else:
            
            return HttpResponseForbidden("Sie haben keine Berechtigung, auf dieses Thema zuzugreifen.")
    else:
        return HttpResponseForbidden("Sie müssen angemeldet sein, um auf dieses Thema zuzugreifen.")