from django.contrib import admin

# Register your models here.
from .models import Doctor, Patient, Specialty, Appointment, Schedule
from django.contrib.auth.models import User


class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ['name']


class DoctorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'middle_name', 'last_name', 'phone_number', 'birth_date', 'qualification', 'specialty']


class PatientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'middle_name', 'last_name', 'phone_number', 'birth_date', 'address']


class AppointmentAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(AppointmentAdmin, self).get_queryset(request)
        if request.user.is_admin:
            return qs
        return qs.filter(doctor=request.user.doctor)
    list_display = ['visit_date', 'visit_time', 'patient', 'doctor', 'status']


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'day_evenness', 'start_time', 'end_time']


admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Schedule, ScheduleAdmin)
