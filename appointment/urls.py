from django.urls import path
from . import views

app_name = "appointment"

urlpatterns = [
    path("", views.home, name="home"),
]