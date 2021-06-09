from datetime import timedelta, datetime, time
from django.shortcuts import render, redirect
from main.models import Specialty, Doctor, Schedule, Patient, Appointment
from .views import get_user_info, my_render


@my_render('order_talon.html')
def order_talon_viewer(request, specialty_id, doctor_id):
    page = OrderTalonPage(specialty_id, doctor_id, request)
    page.show_weeks()
    if request.method == "POST":
        suddenly_taken = False
        if "accept" in request.POST:
            splitted = request.POST.get('accept').split('\\')
            talon_date, talon_time = splitted[0], splitted[1]
            obj = Appointment.objects.filter(visit_date=datetime(int(talon_date[0:4]), int(talon_date[5:7]), int(talon_date[8:10])),
                                          visit_time=time(int(talon_time[0:2]), int(talon_time[3:5])))
            if len(obj) == 0:
                page.make_appointment()
                return page.get_response()
            else:
                suddenly_taken = True
        page.show_talons()
        if "accept" not in request.POST and "talon" not in request.POST:
            return page.get_response()
        if suddenly_taken:
            page.add_to_response({"error_message": "Уупс, ваш талон уже забрали"})
        else:
            page.show_talon_info()
    return page.get_response()


class OrderTalonPage:

    def __init__(self, specialty_id, doctor_id, request):
        self.response = {}
        self.specialty_id = specialty_id
        self.doctor_id = doctor_id
        self.request = request

    def add_to_response(self, attrs):
        self.response = {**self.response, ** attrs}

    def get_response(self):
        return self.response

    def show_weeks(self):
        current_date = datetime.now()
        week1 = []
        week2 = []
        for i in range(14):
            week = week1 if i < 7 else week2
            all_talons, taken_talons, talons = Doctor.get_day_talons(current_date.date(), self.doctor_id, self.specialty_id)
            week.append(type('day', (), {'number': current_date.date().day, 'talons': talons}))
            current_date = get_next_day(current_date)

        self.add_to_response({"week1": week1, "week2": week2})

    def show_talons(self):
        current_date = datetime.now()
        if 'day' in self.request.POST:
            day = self.request.POST.get('day')
        elif 'accept' in self.request.POST:
            day = self.request.POST.get('accept')[8:10]
        else:
            day = self.request.POST.get('talon').split('\\')[0]
        plus_month = 0 if int(day) > int(current_date.day) else 1
        current_date = datetime(year=current_date.year, month=current_date.month + plus_month, day=int(day))
        all_talons, taken_talons, talons = Doctor.get_day_talons(current_date, self.doctor_id, self.specialty_id)

        talons = []
        for talon in all_talons:
            talons.append(type('talon', (), {'time': talon, 'taken': talon in taken_talons, 'day': day}))

        response = {"show_talons": True, "talons": talons, "show_fields": False}
        self.add_to_response(response)

    def show_talon_info(self):
        response = {}
        current_date = datetime.now()
        day = self.request.POST.get('talon').split('\\')[0]
        plus_month = 0 if int(day) > int(current_date.day) else 1
        current_date = datetime(year=current_date.year, month=current_date.month + plus_month, day=int(day))
        all_talons, taken_talons, talons = Doctor.get_day_talons(current_date, self.doctor_id, self.specialty_id)

        if not self.request.user.is_authenticated:
            response["error_message"] = "Зарегестрируйтесь чтобы взять талон!"
            self.add_to_response(response)
            return

        talon_time = self.request.POST.get('talon').split('\\')[1]
        if talon_time[1] == ':':
            talon_time = '0' + talon_time
        if talon_time in [get_hours_and_minutes(talon) for talon in taken_talons]:
            response["error_message"] = "Данное время занято. Выберите другое"
            self.add_to_response(response)
            return

        response["talon_time"] = talon_time
        response["show_fields"] = True
        response["talon_date"] = str(current_date.date())
        response["patient_name"] = "admin" if self.request.user.is_admin else str(Patient.objects.get(user=self.request.user))
        if not self.doctor_id == 0:
            response["doctor_name"] = str(Doctor.objects.get(pk=self.doctor_id))
        else:
            response["doctor_name"] = str(Doctor.pick_random(self.specialty_id, current_date, talon_time))

        self.add_to_response(response)

    def make_appointment(self):
        splitted = self.request.POST.get('accept').split('\\')
        talon_date = splitted[0]
        talon_time = splitted[1]
        if not self.doctor_id == 0:
            doctor = Doctor.objects.get(pk=self.doctor_id)
        else:
            doctor = Doctor.pick_random(self.specialty_id, datetime(int(talon_date[0:4]), int(talon_date[5:7]), int(talon_date[8:10])), talon_time)

        if not self.request.user.is_admin:
            patient = Patient.objects.get(user=self.request.user)
        else:
            patient = None

        Appointment.objects.create(doctor=doctor, patient=patient, visit_date=talon_date, visit_time=talon_time)
        self.add_to_response({"success_message": "Талон успешно заказан"})


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
            return datetime(year=date.year + 1, month=1, day=1)