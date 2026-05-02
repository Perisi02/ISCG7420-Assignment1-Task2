from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr {self.name} - {self.specialty}"

class AppointmentSlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ["date", "start_time"]
        unique_together = ("doctor", "date", "start_time")

    def __str__(self):
        return f"{self.doctor.name} | {self.date} |{self.start_time} - {self.end_time}"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ("Booked", "Booked"),
        ("Cancelled", "Cancelled"),
    ]

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    slot = models.OneToOneField(AppointmentSlot, on_delete=models.CASCADE, related_name="appointment")
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Booked")
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["slot__date", "slot__start_time"]

    def __str__(self):
        return f"{self.patient.username} booked {self.slot}"