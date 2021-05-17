from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.models import User
from authentication.models import Account as User
# from enum import Enum
from collections import defaultdict
from datetime import timedelta, datetime, time


def only_letters_validator(value):
    if value.isalpha():
        return
    raise ValidationError(
        _('поле должно содержать только буквы'),
    )


class Human(models.Model):
    middle_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Фамилия', validators=[only_letters_validator])
    first_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Имя', validators=[only_letters_validator])
    last_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Отчество', validators=[only_letters_validator])
    phone_number = models.CharField(max_length=30, null=False, blank=False, verbose_name='Номер телефона')
    birth_date = models.DateField(max_length=30, null=False, verbose_name='Дата рождения')


class week:
    pass


class Doctor(Human):
    qualifications = (
        ("первая", "первая"),
        ("вторая", "вторая"),
        ("высшая", "высшая"),
    )
    qualification = models.TextField(null=True, blank=True, choices=qualifications, verbose_name='квалификация')
    specialty = models.ForeignKey('Specialty', on_delete=models.PROTECT, default="Null",
                                  verbose_name='специальность', related_name='doctors')
    user = models.OneToOneField(User, default=None, on_delete=models.CASCADE)

    @staticmethod
    def get_day_talons(date, doctor_id, specialty_id):
        if doctor_id == 0:
            return Doctor.get_day_talons_of_all_doctors(date, specialty_id)
        doctor = Doctor.objects.get(pk=doctor_id)
        evenness = int(doctor.schedule.day_evenness)

        start_time = doctor.schedule.start_time
        end_time = doctor.schedule.end_time

        temp = start_time
        appointment_duration = 15
        all_times = []
        while temp < end_time:
            all_times.append(temp)
            if temp.minute + appointment_duration >= 60:
                temp = time(hour=temp.hour + 1, minute=(temp.minute + appointment_duration) % 60)
            else:
                temp = time(hour=temp.hour, minute=temp.minute + appointment_duration)

        appointments = Appointment.objects.filter(doctor=doctor, visit_date=date)
        appointments_datetimes = appointments.values('visit_time')

        taken_times = []
        for i in range(len(appointments_datetimes)):
            app = appointments_datetimes[i]['visit_time']
            take_time = time(hour=app.hour, minute=app.minute)
            taken_times.append(take_time)
        return all_times, taken_times, len(all_times) - len(taken_times)

    @staticmethod
    def get_day_talons_of_all_doctors(date, specialty_id):
        mem = defaultdict(int)
        mem_taken = []
        talons = 0
        for doctor in Doctor.objects.filter(specialty=Specialty.objects.get(pk=specialty_id)):
            all_times, taken_times, tlns = Doctor.get_day_talons(date, doctor.pk, specialty_id)
            talons += tlns
            for time in all_times:
                mem[time] += 1
            for time in taken_times:
                mem_taken.append(time)
                mem[time] -= 1
        res_all_times = []
        res_taken_times = []
        for key, value in mem.items():
            res_all_times.append(key)
        for time in mem_taken:
            if not mem[time]:
                res_taken_times.append(time)
        return res_all_times, res_taken_times, talons

    @staticmethod
    def pick_random(specialty_id, talon_date, talon_time):
        print("pickkkkkkkkkkkkkkkking")
        # possible = []
        for doctor in Doctor.objects.filter(specialty=Specialty.objects.get(pk=specialty_id)):
            all_times, taken_times, tlns = Doctor.get_day_talons(talon_date, doctor.pk, specialty_id)
            if talon_time in [Doctor.get_hours_and_minutes(time) for time in all_times]\
                    and talon_time not in [Doctor.get_hours_and_minutes(time) for time in taken_times]:
                print("Hurray")
                print(doctor)
                # possible.append(doctor)
                return doctor
        # import random
        # return random.choice(possible)
        # return possible.

    @staticmethod
    def get_hours_and_minutes(talon):
        preh = ""
        prem = ""
        if talon.hour < 10:
            preh = '0'
        if talon.minute < 10:
            prem = '0'
        return preh + str(talon.hour) + ':' + prem + str(talon.minute)

    class Meta:
        verbose_name_plural = "Доктора"
        verbose_name = "Доктор"

    def __str__(self):
        return self.middle_name + " " + self.first_name + " " + self.last_name


class Specialty(models.Model):
    name = models.TextField(null=False, blank=False, verbose_name="врач-", validators=[only_letters_validator])

    class Meta:
        verbose_name_plural = "врачебные специльности"
        verbose_name = "специальность"

    def __str__(self):
        return self.name

# class Status(Enum):
#     wasfffffffffffffffffffffffffffffffffffffffffffffffffffffff = 1


class Patient(Human):
    user = models.OneToOneField(User, default=0, on_delete=models.CASCADE)
    address = models.TextField(null=False, blank=False, verbose_name='Адрес')

    class Meta:
        verbose_name_plural = "Пациенты"
        verbose_name = "Пациент"

    def __str__(self):
        return self.middle_name + " " + self.first_name


class Appointment(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.PROTECT, default="Null", verbose_name='пациент')
    doctor = models.ForeignKey('Doctor', on_delete=models.PROTECT, default="Null", verbose_name='доктор')
    # visit_time = models.DateTimeField(verbose_name='время приема')
    visit_date = models.DateField(default=None, verbose_name="день приема")
    visit_time = models.TimeField(default=None, verbose_name="время примема")
    statuses = (
        ("прошел", "прошел"),
        ("не прошел", "не прошел")
    )
    status = models.TextField(null=True, blank=True, choices=statuses, default=statuses[1][0], verbose_name='статус приема')
    cost = models.CharField(max_length=30, null=True, blank=True, verbose_name='Стоимость(руб.)')
    days_to_recover = models.IntegerField(null=True, blank=True, verbose_name='Дней для выздоровления')
    treatment = models.TextField(null=True, blank=True, verbose_name='Лечение')
    
    class Meta:
        verbose_name_plural = 'записи'
        verbose_name = 'запись'
        ordering = ['visit_date', 'visit_time']


class Schedule(models.Model):
    doctor = models.OneToOneField('Doctor', on_delete=models.PROTECT, default="Null", verbose_name='доктор')
    evenness = (
        ("2", "четный"),
        ("1", "нечетный")
    )
    day_evenness = models.CharField(max_length=30, null=True, blank=True, choices=evenness, verbose_name='день')
    start_time = models.TimeField(verbose_name='начало рабочего дня')
    end_time = models.TimeField(verbose_name='конец рабочего дня')

    class Meta:
        verbose_name_plural = 'график врачей'
        verbose_name = 'расписание врача'

    def __str__(self):
        return str(self.doctor)
