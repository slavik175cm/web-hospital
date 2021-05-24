from django.shortcuts import render, redirect
from main.models import Specialty, Doctor, Schedule, Patient, Appointment
import copy
# import urllib.request
# import json


# def get_covid_data():
#     response = urllib.request.urlopen('https://covid2019-api.herokuapp.com/v2/country/belarus')
#     data = json.loads(response.read().decode('UTF-8'))["data"]
def get_user_info(request):
    username = ""
    if request.user.is_authenticated:
        if request.user.is_admin:
            username = "admin"
        else:
            username = str(Patient.objects.get(user=request.user))
    res = {"is_user_authenticated": request.user.is_authenticated, "username": username}
    return res


def my_render(template_name):
    def inner_render(function_to_decorate):
        def wrapper(*args, **kwargs):
            request = args[0]
            return render(request, template_name,
                          {**function_to_decorate(*args, **kwargs), **get_user_info(request)})

        return wrapper
    return inner_render


@my_render('info.html')
def info_viewer(request):
    return {}


@my_render('doctors.html')
def doctors_viewer(request):
    departments = []
    specialties = Specialty.objects.all()
    for specialty in specialties:
        doctor = Doctor.objects.filter(specialty=specialty)
        departments.append(type('Department', (), {'specialty': specialty, 'doctors': doctor}))
    return {'departments': departments}


@my_render('schedule.html')
def schedule_viewer(request):
    departments = []
    specialties = Specialty.objects.all()
    for specialty in specialties:
        schedules = []
        doctors = Doctor.objects.filter(specialty=specialty)
        for doctor in doctors:
            schedule = Schedule.objects.get(doctor=doctor)
            schedules.append(schedule)

        departments.append(type('Department', (), {'specialty': specialty, 'schedules': copy.deepcopy(schedules)}))
    return {'departments': departments}


@my_render('order_specialties.html')
def order_specialties_viewer(request):
    all_specialties = Specialty.objects.all()
    return {'all_specialties': all_specialties}


@my_render('order_doctors.html')
def order_doctors_viewer(request, specialty_id):
    specialty = Specialty.objects.get(pk=specialty_id)
    if specialty_id == 0:
        doctors = Doctor.objects.all()
    else:
        doctors = Doctor.objects.filter(specialty=specialty)

    return {'specialty': specialty, 'doctors': doctors}


@my_render('history.html')
def history_viewer(request):
    appointments = Appointment.objects.filter(patient=request.user.patient)
    response = []
    for appointment in appointments:
        response.append(appointment.visit_time)
    return {"appointments": appointments}


def redirect_to_info(request):
    return redirect('info/')
