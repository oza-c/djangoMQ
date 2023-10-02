from django.urls import path
from . import views


app_name="web"
urlpatterns = [
    path("", views.index, name="index" ),
    path("login/", views.login_funktion, name="login"),
    path("register/", views.register_funktion, name="register"),
    path("logout/", views.logOut_view, name="logout")
]