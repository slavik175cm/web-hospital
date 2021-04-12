from django.urls import path
from .views import info_viewer, doctors_viewer, schedule_viewer, \
    order_specialties_viewer, order_doctors_viewer, order_calendar_viewer

urlpatterns = [
    path('info/', info_viewer),
    path('doctors/', doctors_viewer),
    path('schedule/', schedule_viewer),
    path('order/', order_specialties_viewer),
    path('order/<int:specialty_id>', order_doctors_viewer),
    path('order/<int:specialty_id>/<int:doctor_id>', order_calendar_viewer),

]
