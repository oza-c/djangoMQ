# Generated by Django 4.2.4 on 2023-09-08 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mqtt', '0002_brokerconnectionsettingsmodel_broker_port_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brokerconnectionsettingsmodel',
            name='broker_port',
            field=models.BigIntegerField(default=1883),
        ),
    ]
