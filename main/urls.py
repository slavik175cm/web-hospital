from django.urls import path
from main.views import info_viewer, doctors_viewer, schedule_viewer, \
    order_specialties_viewer, order_doctors_viewer, order_talon_viewer, \
    redirect_to_info, history_viewer, profile_viewer

urlpatterns = [
    path('', redirect_to_info),
    path('info/', info_viewer, name="info"),
    path('doctors/', doctors_viewer, name="doctor"),
    path('schedule/', schedule_viewer, name="schedule"),
    path('order/', order_specialties_viewer, name="order specialties"),
    path('order/<int:specialty_id>', order_doctors_viewer),
    path('order/<int:specialty_id>/<int:doctor_id>', order_talon_viewer),
    path('history/', history_viewer, name="history"),
    path('profile/<int:user_id>', profile_viewer, name="profile")
]
