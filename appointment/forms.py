from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Appointment, Doctor, AppointmentSlot


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["reason"]
        widgets = {
            "reason": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Optional: briefly describe the reason for your appointment"
            }),
        }


class PatientRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your email address"
        })
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Choose a username"
            }),
        }

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ["name", "specialty", "phone", "email", "bio", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter doctor's name"
            }),
            "specialty": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter specialty"
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter phone number"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter email address"
            }),
            "bio": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Enter doctor bio"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }

class AppointmentSlotForm(forms.ModelForm):
    class Meta:
        model = AppointmentSlot
        fields = ["doctor", "date", "start_time", "end_time", "is_available"]
        widgets = {
            "doctor": forms.Select(attrs={
                "class": "form-control"
            }),
            "date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "start_time": forms.TimeInput(attrs={
                "class": "form-control",
                "type": "time"
            }),
            "end_time": forms.TimeInput(attrs={
                "class": "form-control",
                "type": "time"
            }),
            "is_available": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }