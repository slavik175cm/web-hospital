from django.shortcuts import render, redirect
from main.models import Specialty, Doctor, Schedule, Patient, Appointment
import copy
from django.contrib.sessions.models import Session
import urllib.request
import json
import threading
import concurrent.futures


def receive_covid_data(func, *args, **kwargs):
    print("string urlopen")
    response = urllib.request.urlopen('https://covid2019-api.herokuapp.com/v2/country/belarus')
    data = json.loads(response.read().decode('UTF-8'))["data"]
    request = args[0]
    request.session['loaded'] = True
    request.session['cases'] = data['confirmed']
    request.session['recovered'] = data['recovered']
    request.session['deaths'] = data['deaths']

    request.session.save()
    print(request.session.items())


def get_covid_data(request):
    if not request.session.__contains__('loaded'):
        return {None: None}
    else:
        return {"show_covid": True, "cases": request.session['cases'], "recovered": request.session['recovered'],
                "deaths": request.session['deaths']}


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
            # print("!!!!!!!!!!!", request.session.items())
            # request.session.flush()
            # if not request.session.__contains__('loading'):
            #     request.session['loading'] = True
            #     my_thread = threading.Thread(target=receive_covid_data, args=(function_to_decorate, *args))
            #     my_thread.start()
            return render(request, template_name,
                          {**function_to_decorate(*args, **kwargs),
                           **get_user_info(request),
                           # **get_covid_data(request),
                           })

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
    if request.method == "POST":
        pk = int(request.POST.get('pk_to_delete'))
        Appointment.objects.get(pk=pk).delete()
    appointments = Appointment.objects.filter(patient=request.user.patient)
    return {"appointments": appointments}


def redirect_to_info(request):
    return redirect('info/')
