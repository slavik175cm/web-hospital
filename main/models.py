from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# from enum import Enum


def only_letters_validator(value):
    if value.isalpha():
        return
    raise ValidationError(
        _('поле должно содержать только буквы'),
    )


class Human(models.Model):
    middle_name = models.TextField(null=False, blank=False, verbose_name='Фамилия', validators=[only_letters_validator])
    first_name = models.TextField(null=False, blank=False, verbose_name='Имя', validators=[only_letters_validator])
    last_name = models.TextField(null=False, blank=False, verbose_name='Отчество', validators=[only_letters_validator])
    phone_number = models.TextField(null=False, blank=False, verbose_name='Номер телефона')
    birth_date = models.DateField(verbose_name='Дата рождения')


class Doctor(Human):
    qualifications = (
        ("первая", "первая"),
        ("вторая", "вторая"),
        ("высшая", "высшая")
    )
    qualification = models.TextField(null=True, blank=True, choices=qualifications, verbose_name='квалификация')
    specialty = models.ForeignKey('Specialty', on_delete=models.PROTECT, default="Null",
                                  verbose_name='специальность', related_name='doctors')

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
    address = models.TextField(null=False, blank=False, verbose_name='Адрес')

    class Meta:
        verbose_name_plural = "Пациенты"
        verbose_name = "Пациент"

    def __str__(self):
        return self.middle_name + " " + self.first_name


class Appointment(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.PROTECT, default="Null", verbose_name='пациент')
    doctor = models.ForeignKey('Doctor', on_delete=models.PROTECT, default="Null", verbose_name='доктор')
    visit_time = models.DateTimeField(verbose_name='время приема')
    statuses = (
        ("прошел", "прошел"),
        ("не прошел", "не прошел")
    )
    status = models.TextField(null=True, blank=True, choices=statuses, verbose_name='статус приема')
    cost = models.TextField(null=True, blank=True, verbose_name='Стоимость(руб.)')
    days_to_recover = models.IntegerField(null=True, blank=True, verbose_name='Дней для выздоровления')
    treatment = models.TextField(null=True, blank=True, verbose_name='Лечение')
    
    class Meta:
        verbose_name_plural = 'записи'
        verbose_name = 'запись'
        ordering = ['visit_time']


class Schedule(models.Model):
    doctor = models.OneToOneField('Doctor', on_delete=models.PROTECT, default="Null", verbose_name='доктор')
    evenness = (
        ("четный", "четный"),
        ("нечетный", "нечетный")
    )
    day_evenness = models.TextField(null=True, blank=True, choices=evenness, verbose_name='день')
    start_time = models.TimeField(verbose_name='начало рабочего дня')
    end_time = models.TimeField(verbose_name='конец рабочего дня')

    class Meta:
        verbose_name_plural = 'график врачей'
        verbose_name = 'расписание врача'

    def __str__(self):
        return self.day_evenness
