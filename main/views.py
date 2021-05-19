from django.shortcuts import render, redirect
from .models import Specialty, Doctor, Schedule, Patient, Appointment
import copy
from datetime import timedelta, datetime, time

import urllib.request
import json

def get_covid_data():
    response = urllib.request.urlopen('https://covid2019-api.herokuapp.com/v2/country/belarus')
    data = json.loads(response.read().decode('UTF-8'))["data"]
    print(data["confirmed"])
    print(data["deaths"])
    print(data["recovered"])
    print(data)


def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z


def get_user_info(request):
    username = ""
    if request.user.is_authenticated:
        if request.user.is_admin:
            username = "admin"
        else:
            username = str(Patient.objects.get(user=request.user))
    res = {"is_user_authenticated": request.user.is_authenticated, "username": username}
    return res


def info_viewer(request):
    # get_covid_data()
    username = ""
    if request.user.is_authenticated:
        if request.user.is_admin:
            username = "admin"
        else:
            username = str(Patient.objects.get(user=request.user))
    return render(request, 'info.html', merge_two_dicts({}, get_user_info(request)))


class Department:
    pass


def doctors_viewer(request):
    departments = []
    specialties = Specialty.objects.all()
    for specialty in specialties:
        doctor = Doctor.objects.filter(specialty=specialty)

        department = Department()
        department.__setattr__('specialty', specialty)
        department.__setattr__('doctors', doctor)
        departments.append(department)

    return render(request, 'doctors.html', merge_two_dicts({'departments': departments}, get_user_info(request)))


def schedule_viewer(request):
    # doctors_schedule = Schedule.objects.all()
    # return render(request, 'schedule.html', {'doctors_schedule': doctors_schedule})
    departments = []
    specialties = Specialty.objects.all()
    for specialty in specialties:
        schedules = []
        doctors = Doctor.objects.filter(specialty=specialty)
        for doctor in doctors:
            schedule = Schedule.objects.get(doctor=doctor)
            schedules.append(schedule)

        department = Department()
        department.__setattr__('specialty', specialty)
        department.__setattr__('schedules', copy.deepcopy(schedules))
        departments.append(department)

    return render(request, 'schedule.html', merge_two_dicts({'departments': departments}, get_user_info(request)))


def order_specialties_viewer(request):
    all_specialties = Specialty.objects.all()
    # sp = Specialty.objects.filter(pk=specialty_id)
    # doctors = Doctor.objects.filter(specialty=sp)
    return render(request, 'order_specialties.html', merge_two_dicts({'all_specialties': all_specialties}, get_user_info(request)))


def order_doctors_viewer(request, specialty_id):
    specialty = Specialty.objects.get(pk=specialty_id)
    if specialty_id == 0:
        doctors = Doctor.objects.all()
    else:
        doctors = Doctor.objects.filter(specialty=specialty)

    return render(request, 'order_doctors.html', merge_two_dicts({'specialty': specialty, 'doctors': doctors}, get_user_info(request)))


class Day:
    pass


def order_calendar_viewer(request, specialty_id, doctor_id):
    current_date = datetime.now()
    week1 = []
    week2 = []
    for i in range(7):
        all_talons, taken_talons, talons = Doctor.get_day_talons(current_date.date(), doctor_id, specialty_id)
        day = Day()
        day.__setattr__('number', current_date.date().day)
        day.__setattr__('talons', talons)
        week1.append(day)
        current_date = get_next_day(current_date)

    for i in range(7):
        all_talons, taken_talons, talons = Doctor.get_day_talons(current_date.date(), doctor_id, specialty_id)
        day = Day()
        day.__setattr__('number', current_date.date().day)
        day.__setattr__('talons', talons)
        week2.append(day)
        current_date = get_next_day(current_date)
        # current_date = datetime(year=current_date.year, month=current_date.month, day=current_date.day + 1)

    show_talons = False
    show_fields = False
    talons = []
    doctor_name = ""
    patient_name = ""
    talon_time = ""
    talon_date = ""
    success_message = ""
    if request.method == "POST":
        if "accept" in request.POST:
            splitted = request.POST.get('accept').split('\\')
            talon_date = splitted[0]
            talon_time = splitted[1]
            print("HERE")
            if not doctor_id == 0:
                doctor = Doctor.objects.get(pk=doctor_id)
            else:
                doctor = Doctor.pick_random(specialty_id, talon_date, talon_time)
            print("taken")
            print(doctor)
            if not request.user.is_admin:
                patient = Patient.objects.get(user=request.user)
            else:
                patient = None

            Appointment.objects.create(doctor=doctor, patient=patient, visit_date=talon_date, visit_time=talon_time)
            success_message = "Талон успешно заказан"
            return render(request, 'order_calendar.html', merge_two_dicts({'week1': week1, 'week2': week2,
                                                    "show_talons": show_talons, "talons": talons,
                                                    "show_fields": show_fields, 'doctor_name': doctor_name,
                                                    "patient_name": patient_name, "talon_time": talon_time,
                                                    "talon_date": talon_date, "success_message":success_message}, get_user_info(request)))
        print(request.POST)
        show_talons = True
        current_date = datetime.now()
        if "day" in request.POST:
            day = request.POST.get('day')
        else:
            day = request.POST.get('talon').split('\\')[0]

        current_date = datetime(year=current_date.year, month=current_date.month, day=int(day))

        all_talons, taken_talons, talons = Doctor.get_day_talons(current_date, doctor_id, specialty_id)

        class Talon:
            pass

        talons = []
        for talon in all_talons:
            tln = Talon()
            tln.__setattr__('time', talon)
            tln.__setattr__('taken', talon in taken_talons)
            tln.__setattr__('day', day)
            talons.append(tln)

        if "talon" in request.POST:
            if not request.user.is_authenticated:
                return render(request, 'order_calendar.html', merge_two_dicts({'week1': week1, 'week2': week2,
                                                                               "show_talons": show_talons,
                                                                               "talons": talons,
                                                                               "show_fields": show_fields,
                                                                               'doctor_name': doctor_name,
                                                                               "patient_name": patient_name,
                                                                               "talon_time": talon_time,
                                                                               "talon_date": talon_date,
                                                                               "error_message": "Зарегестрируйтесь чтобы взять талон!"},
                                                                              get_user_info(request)))

            talon_time = request.POST.get('talon').split('\\')[1]
            if talon_time[1] == ':':
                talon_time = '0' + talon_time
            if talon_time in [get_hours_and_minutes(talon) for talon in taken_talons]:
                return render(request, 'order_calendar.html', merge_two_dicts({'week1': week1, 'week2': week2,
                                                                               "show_talons": show_talons,
                                                                               "talons": talons,
                                                                               "show_fields": show_fields,
                                                                               'doctor_name': doctor_name,
                                                                               "patient_name": patient_name,
                                                                               "talon_time": talon_time,
                                                                               "talon_date": talon_date,
                                                                               "error_message": "Данное время занято. Выберите другое"},
                                                                              get_user_info(request)))
            show_fields = True
            talon_date = str(current_date.date())
            if not request.user.is_admin:
                patient_name = str(Patient.objects.get(user=request.user))
            else:
                patient_name = "admin"
            if not doctor_id == 0:
                doctor_name = str(Doctor.objects.get(pk=doctor_id))
            else:
                doctor_name = str(Doctor.pick_random(specialty_id, current_date, talon_time))

    return render(request, 'order_calendar.html', merge_two_dicts({'week1': week1, 'week2': week2,
                                                   "show_talons": show_talons, "talons": talons,
                                                   "show_fields": show_fields, 'doctor_name': doctor_name,
                                                   "patient_name": patient_name, "talon_time": talon_time,
                                                   "talon_date": talon_date},
                                                                  get_user_info(request)))


def get_hours_and_minutes(talon):
    preh = ""
    prem = ""
    if talon.hour < 10:
        preh = '0'
    if talon.minute < 10:
        prem = '0'
    return preh + str(talon.hour) + ':' + prem + str(talon.minute)


def get_next_day(date):
    try:
        return datetime(year=date.year, month=date.month, day=date.day + 1)
    except:
        try:
            return datetime(year=date.year, month=date.month+1, day=1)
        except:
            return datetime(year=date.year, month=1, day=1)


def redirect_viewer(request):
    response = redirect('info/')
    return response


def history_viewer(request):
    appointments = Appointment.objects.filter(patient=request.user.patient)
    response = []
    for appointment in appointments:
        response.append(appointment.visit_time)
    return render(request, 'history.html', merge_two_dicts({"appointments": appointments}, get_user_info(request)))
