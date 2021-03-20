from django.shortcuts import render
from .models import Specialty, Doctor, Schedule


def info_viewer(request):
    # specialties = Specialty.objects.all()
    return render(request, 'info.html', {})


def doctors_viewer(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctors.html', {'doctors': doctors})


def schedule_viewer(request):
    doctors_schedule = Schedule.objects.all()
    return render(request, 'schedule.html', {'doctors_schedule': doctors_schedule})


def order_viewer(request, specialty_id):
    all_specialties = Specialty.objects.all()
    # sp = Specialty.objects.filter(pk=specialty_id)
    # doctors = Doctor.objects.filter(specialty=sp)
    if specialty_id == 0:
        doctors = Doctor.objects.all()
    else:
        specialty = Specialty.objects.filter(pk=specialty_id)
        doctors = specialty[0].doctors.all()

    return render(request, 'order.html', {'all_specialties': all_specialties, 'doctors': doctors})
