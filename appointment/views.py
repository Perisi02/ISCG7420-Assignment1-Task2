from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Doctor, AppointmentSlot, Appointment
from .forms import AppointmentForm


# Create your views here.
def home(request):
    return render(request, "appointment/home.html")


def doctor_list(request):
    doctors = Doctor.objects.filter(is_active=True).order_by("name")
    return render(request, "appointment/doctor_list.html", {"doctors": doctors})


def slot_list(request):
    slots = AppointmentSlot.objects.filter(is_available=True).select_related("doctor").order_by("date", "start_time")

    return render(request, "appointment/slot_list.html", {"slots": slots})


@login_required
def book_appointment(request, slot_id):
    slot = get_object_or_404(AppointmentSlot, id=slot_id)

    if not slot.is_available or hasattr(slot, "appointment"):
        messages.error(request, "Sorry, this appointment slot has already been booked.")
        return redirect("appointment:slot_list")

    if request.method == "POST":
        form = AppointmentForm(request.POST)

        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.slot = slot
            appointment.save()

            slot.is_available = False
            slot.save()

            messages.success(request, "Your appointment has been booked successfully.")
            return redirect("appointment:my_appointments")
    else:
        form = AppointmentForm()

    return render(request, "appointment/book_appointment.html", {
        "form": form,
        "slot": slot
    })


@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(
        patient=request.user
    ).select_related("slot", "slot__doctor").order_by("slot__date", "slot__start_time")

    return render(request, "appointment/my_appointments.html", {
        "appointments": appointments
    })
