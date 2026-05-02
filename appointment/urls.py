from django.urls import path
from . import views

app_name = "appointment"

urlpatterns = [
    path("", views.home, name="home"),
    path("doctors/", views.doctor_list, name="doctor_list"),
    path("slots/", views.slot_list, name="slot_list"),
    path("slots/<int:slot_id>/book/", views.book_appointment, name="book_appointment"),
    path("my-appointments/", views.my_appointments, name="my_appointments"),
    path("appointments/<int:appointment_id>/edit/", views.edit_appointment, name="edit_appointment"),
    path("appointments/<int:appointment_id>/cancel/", views.cancel_appointment, name="cancel_appointment"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/doctors/", views.manage_doctors, name="manage_doctors"),
    path("dashboard/doctors/add/", views.add_doctor, name="add_doctor"),
    path("dashboard/doctors/<int:doctor_id>/edit/", views.edit_doctor, name="edit_doctor"),
    path("dashboard/doctors/<int:doctor_id>/delete/", views.delete_doctor, name="delete_doctor"),
    path("dashboard/slots/", views.manage_slots, name="manage_slots"),
    path("dashboard/slots/add/", views.add_slot, name="add_slot"),
    path("dashboard/slots/<int:slot_id>/edit/", views.edit_slot, name="edit_slot"),
    path("dashboard/slots/<int:slot_id>/delete/", views.delete_slot, name="delete_slot"),
]
