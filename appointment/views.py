from django.shortcuts import render

from appointment.models import Doctor


# Create your views here.
def home(request):
    return render(request, 'appointment/home.html')

def doctor_list(request):
    doctors = Doctor.objects.filter(is_active=True).order_by('name')
    return render(request, 'appointment/doctor_list.html', {'doctors': doctors})