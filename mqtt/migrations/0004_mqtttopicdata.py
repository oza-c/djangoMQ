# Generated by Django 4.2.4 on 2023-09-08 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0007_rename_m_name_topicmodel_topic_name'),
        ('mqtt', '0003_alter_brokerconnectionsettingsmodel_broker_port'),
    ]

    operations = [
        migrations.CreateModel(
            name='mqttTopicData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mqtt_timestamp', models.CharField(max_length=50)),
                ('mqtt_payload', models.CharField(max_length=50)),
                ('mqtt_topic', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='topics.topicmodel')),
            ],
        ),
    ]