from django.core.management.base import BaseCommand
from mqtt.mqtt_helper import connect_clients

# Globale Flag, um sicherzustellen, dass connect_clients() nur einmal aufgerufen wird
has_connected_clients = False

class Command(BaseCommand):
    help = 'Starts the Django development server and runs custom code'

    def handle(self, *args, **kwargs):
        global has_connected_clients
        self.stdout.write(self.style.SUCCESS('Starting the Django development server...'))

        # Nur verbinden, wenn es noch nicht geschehen ist
        if not has_connected_clients:
            connect_clients()
            has_connected_clients = True

        # Starten Sie den Django-Entwicklungsserver
        from django.core.management import call_command
        call_command('runserver', *args, **kwargs)
