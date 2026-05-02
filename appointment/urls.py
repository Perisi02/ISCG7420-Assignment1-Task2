from django.urls import path
from . import views

app_name = "appointment"

urlpatterns = [
    path("", views.home, name="home"),
    path("doctors/", views.doctor_list, name="doctor_list"),
    path("slots/", views.slot_list, name="slot_list"),
]