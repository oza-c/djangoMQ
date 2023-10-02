from django.urls import path
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

app_name="topics"
urlpatterns = [
    path("", views.index, name="index" ),
    path("topic_hinzufuegen", views.topic_hinzufuegen, name="topic_hinzufuegen"),
    path("loeschen/<int:id>", views.topic_loeschen, name="loeschen"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("settings", views.settings, name="settings"),
    path("settings/change", views.settings_change, name="settings_change"),
    path("<str:topicname>", views.detailTopic, name="detail"),
    path('favicon.ico',RedirectView.as_view(url='/static/images/favicon.ico')),
]