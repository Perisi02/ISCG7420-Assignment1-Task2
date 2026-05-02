from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from .models import Doctor, AppointmentSlot, Appointment
from .forms import AppointmentForm, PatientRegistrationForm, DoctorForm, AppointmentSlotForm


# Create your views here.
def home(request):
    return render(request, "appointment/home.html")


def doctor_list(request):
    doctors = Doctor.objects.filter(is_active=True).order_by("name")
    return render(request, "appointment/doctor_list.html", {"doctors": doctors})


def slot_list(request):
    slots = AppointmentSlot.objects.filter(
        is_available=True,
        appointment__isnull=True
    ).select_related("doctor").order_by("date", "start_time")

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


def register(request):
    if request.method == "POST":
        form = PatientRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect("appointment:home")
    else:
        form = PatientRegistrationForm()

    return render(request, "registration/register.html", {
        "form": form
    })

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient=request.user
    )

    if request.method == "POST":
        slot = appointment.slot
        appointment.status = "Cancelled"
        appointment.save()

        slot.is_available = True
        slot.save()

        appointment.delete()

        messages.success(request, "Your appointment has been cancelled.")
        return redirect("appointment:my_appointments")

    return render(request, "appointment/cancel_appointment.html", {
        "appointment": appointment
    })

@login_required
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient=request.user
    )

    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)

        if form.is_valid():
            form.save()
            messages.success(request, "Your appointment has been updated.")
            return redirect("appointment:my_appointments")
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, "appointment/edit_appointment.html", {
        "form": form,
        "appointment": appointment
    })

def staff_required(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(staff_required)
def dashboard(request):
    doctor_count = Doctor.objects.count()
    slot_count = AppointmentSlot.objects.count()
    appointment_count = Appointment.objects.count()
    patient_count = User.objects.filter(is_staff=False).count()

    return render(request, "appointment/dashboard.html", {
        "doctor_count": doctor_count,
        "slot_count": slot_count,
        "appointment_count": appointment_count,
        "patient_count": patient_count,
    })

@user_passes_test(staff_required)
def manage_doctors(request):
    doctors = Doctor.objects.all().order_by("name")

    return render(request, "appointment/manage_doctors.html", {
        "doctors": doctors
    })


@user_passes_test(staff_required)
def add_doctor(request):
    if request.method == "POST":
        form = DoctorForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Doctor profile has been added.")
            return redirect("appointment:manage_doctors")
    else:
        form = DoctorForm()

    return render(request, "appointment/doctor_form.html", {
        "form": form,
        "title": "Add Doctor"
    })


@user_passes_test(staff_required)
def edit_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == "POST":
        form = DoctorForm(request.POST, instance=doctor)

        if form.is_valid():
            form.save()
            messages.success(request, "Doctor profile has been updated.")
            return redirect("appointment:manage_doctors")
    else:
        form = DoctorForm(instance=doctor)

    return render(request, "appointment/doctor_form.html", {
        "form": form,
        "title": "Edit Doctor"
    })


@user_passes_test(staff_required)
def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == "POST":
        doctor.delete()
        messages.success(request, "Doctor profile has been deleted.")
        return redirect("appointment:manage_doctors")

    return render(request, "appointment/delete_doctor.html", {
        "doctor": doctor
    })

@user_passes_test(staff_required)
def manage_slots(request):
    slots = AppointmentSlot.objects.select_related("doctor").order_by("date", "start_time")

    return render(request, "appointment/manage_slots.html", {
        "slots": slots
    })


@user_passes_test(staff_required)
def add_slot(request):
    if request.method == "POST":
        form = AppointmentSlotForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Appointment slot has been added.")
            return redirect("appointment:manage_slots")
    else:
        form = AppointmentSlotForm()

    return render(request, "appointment/slot_form.html", {
        "form": form,
        "title": "Add Appointment Slot"
    })


@user_passes_test(staff_required)
def edit_slot(request, slot_id):
    slot = get_object_or_404(AppointmentSlot, id=slot_id)

    if request.method == "POST":
        form = AppointmentSlotForm(request.POST, instance=slot)

        if form.is_valid():
            form.save()
            messages.success(request, "Appointment slot has been updated.")
            return redirect("appointment:manage_slots")
    else:
        form = AppointmentSlotForm(instance=slot)

    return render(request, "appointment/slot_form.html", {
        "form": form,
        "title": "Edit Appointment Slot"
    })


@user_passes_test(staff_required)
def delete_slot(request, slot_id):
    slot = get_object_or_404(AppointmentSlot, id=slot_id)

    if request.method == "POST":
        slot.delete()
        messages.success(request, "Appointment slot has been deleted.")
        return redirect("appointment:manage_slots")

    return render(request, "appointment/delete_slot.html", {
        "slot": slot
    })