from django.shortcuts import render

from appointment.models import Doctor, AppointmentSlot


# Create your views here.
def home(request):
    return render(request, 'appointment/home.html')

def doctor_list(request):
    doctors = Doctor.objects.filter(is_active=True).order_by('name')
    return render(request, 'appointment/doctor_list.html', {'doctors': doctors})

def slot_list(request):
    slots = AppointmentSlot.objects.filter(is_available=True).select_related('doctor').order_by('date', 'start_time')
    return render(request, 'appointment/slot_list.html', {'slots': slots})