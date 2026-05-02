from django.contrib import admin
from .models import Doctor, Appointment, AppointmentSlot

# Register your models here.
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("name", "specialty", "email", "phone", "is_active")
    search_fields = ("name", "specialty")
    list_filter = ("specialty", "is_active")


@admin.register(AppointmentSlot)
class AppointmentSlotAdmin(admin.ModelAdmin):
    list_display = ("doctor", "date", "start_time", "end_time", "is_available")
    list_filter = ("date", "doctor", "is_available")
    search_fields = ("doctor__name",)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "slot", "status", "booked_at")
    list_filter = ("status", "slot__date")
    search_fields = ("patient__username", "slot__doctor__name")
