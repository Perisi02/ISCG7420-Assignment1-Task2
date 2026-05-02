from django import forms
from .models import Appointment


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