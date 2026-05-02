from django.urls import path
from . import views

app_name = "appointment"

urlpatterns = [
    path("", views.home, name="home"),
    path("doctors/", views.doctor_list, name="doctor_list"),
    path("slots/", views.slot_list, name="slot_list"),
    path("slots/<int:slot_id>/book/", views.book_appointment, name="book_appointment"),
    path("my-appointments/", views.my_appointments, name="my_appointments"),
]