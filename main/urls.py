from django.urls import path
from .views import info_viewer, doctors_viewer, schedule_viewer, order_viewer

urlpatterns = [
    path('info/', info_viewer),
    path('doctors/', doctors_viewer),
    path('schedule/', schedule_viewer),
    path('order/<int:specialty_id>', order_viewer),

]
