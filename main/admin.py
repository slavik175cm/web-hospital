from django.contrib import admin

# Register your models here.
from .models import Doctor, Patient, Specialty, Appointment, Schedule


class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ['name']


class DoctorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'middle_name', 'last_name', 'phone_number', 'birth_date', 'qualification', 'specialty']


class PatientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'middle_name', 'last_name', 'phone_number', 'birth_date', 'address']


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['visit_time', 'patient', 'doctor', 'status']


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'day_evenness', 'start_time', 'end_time']


admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Schedule, ScheduleAdmin)
