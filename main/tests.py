from django.http import request, response
from django.test import RequestFactory
from django.urls import reverse, resolve
from django.contrib.auth.models import User, AnonymousUser
from .views import info_viewer
from authentication.models import Account
from .models import Patient, Doctor, Specialty, Schedule
from .views import profile_viewer
from .views.order_talon_view import order_talon_viewer
from datetime import timedelta, datetime, time
from .forms import ProfileForm
from django.contrib.auth import login, authenticate
import pytest

url_names = ["info", "doctor", "schedule", "order specialties", "history"]
class Test:
    @pytest.mark.django_db
    def test_1(self):
        self.factory = RequestFactory()
        Account.objects.create(email="user@gmail.com", username="user", password="123")
        me = Account.objects.get(email='user@gmail.com')
        Patient.objects.create(user=me, first_name="aa", last_name="aa", middle_name="aa",
                               phone_number=123, address="123", birth_date=datetime.now())
        Account.objects.create(email="user1@gmail.com", username="user", password="123")
        doc = Account.objects.get(email="user1@gmail.com")
        Specialty.objects.create(name="hirurg")
        specialty = Specialty.objects.get(name="hirurg")
        Doctor.objects.create(user=doc, first_name="aa", last_name="aa", middle_name="aa",
                               phone_number=123, birth_date=datetime.now(),
                              specialty=specialty, qualification="firs")
        Schedule.objects.create(doctor=Doctor.objects.get(user=doc), day_evenness="chetn",
                                start_time=datetime.now(), end_time=datetime.now())
        # me = Patient.objects.get(user=me)
        for url in url_names:
            path = reverse(url)
            request = self.factory.get(path)
            request.user = me
            viewer = resolve(path).func
            response = viewer(request)
            assert response.status_code == 200

    @pytest.mark.django_db
    def test_2(self):
        self.factory = RequestFactory()
        from django.contrib.auth.hashers import make_password
        Account.objects.create(email="user@gmail.com", username="user", password=make_password("123"))
        me = Account.objects.get(email='user@gmail.com')
        Patient.objects.create(user=me, first_name="aa", last_name="aa", middle_name="aa",
                               phone_number=123, address="123", birth_date=datetime.now())


        request = self.factory.post("profile/<int:user_id>", {"password": "123", "new_password1": "",
                                                              "new_password2": "",
                             "first_name": "asdf", "middle_name": "adsf", "last_name": "adsf",
                             "phone_number": "+123456789123", "birth_date": datetime(year=2002, month=10, day=3).date(),
                             "address": "asdf"})
        me._is_authenticated = True
        request.user = me
        response = profile_viewer(request, 1)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_3(self):
        self.factory = RequestFactory()
        Account.objects.create(email="user@gmail.com", username="user", password="123")
        me = Account.objects.get(email='user@gmail.com')
        Patient.objects.create(user=me, first_name="aa", last_name="aa", middle_name="aa",
                               phone_number=123, address="123", birth_date=datetime.now())
        Account.objects.create(email="user1@gmail.com", username="user", password="123")
        doc = Account.objects.get(email="user1@gmail.com")
        Specialty.objects.create(name="hirurg")
        specialty = Specialty.objects.get(name="hirurg")
        Doctor.objects.create(user=doc, first_name="aa", last_name="aa", middle_name="aa",
                              phone_number=123, birth_date=datetime.now(),
                              specialty=specialty, qualification="firs")
        Schedule.objects.create(doctor=Doctor.objects.get(user=doc), day_evenness="2",
                                start_time=datetime.now(), end_time=datetime.now())

        request = self.factory.get("order/<int:specialty_id>/<int:doctor_id>")
        # me._is_authenticated = True
        request.user = me
        response = order_talon_viewer(request, 1, 2)
        assert response.status_code == 200

        request = self.factory.get("order/<int:specialty_id>/<int:doctor_id>")
        # me._is_authenticated = True
        request.user = me
        response = order_talon_viewer(request, 1, 0)
        assert response.status_code == 200

        request = self.factory.post("order/<int:specialty_id>/<int:doctor_id>", {"talon": "10\\10:15"})
        # me._is_authenticated = True
        request.user = me
        response = order_talon_viewer(request, 1, 2)
        assert response.status_code == 200

        request = self.factory.post("order/<int:specialty_id>/<int:doctor_id>", {"accept": "2021-06-09\\10:15"})
        # me._is_authenticated = True
        request.user = me
        response = order_talon_viewer(request, 1, 2)
        assert response.status_code == 200





