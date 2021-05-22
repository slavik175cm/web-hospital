from django.urls import path
from .views import info_viewer, doctors_viewer, schedule_viewer, \
    order_specialties_viewer, order_doctors_viewer, order_talon_viewer, \
    redirect_to_info, history_viewer

urlpatterns = [
    path('', redirect_to_info),
    path('info/', info_viewer),
    path('doctors/', doctors_viewer),
    path('schedule/', schedule_viewer),
    path('order/', order_specialties_viewer),
    path('order/<int:specialty_id>', order_doctors_viewer),
    path('order/<int:specialty_id>/<int:doctor_id>', order_talon_viewer),
    path('history/', history_viewer),

]
