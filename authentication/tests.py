from django.http import request, response
from django.test import RequestFactory
from django.urls import reverse, resolve
from django.contrib.auth.models import User, AnonymousUser
from .models import Account, MyAccountManager
from .forms import RegistrationForm, PatientRegistrationForm
from .views import login_viewer
import pytest


class Test:
    def test_1(self):
        self.factory = RequestFactory()
        request = self.factory.get('/admin')
        response = login_viewer(request)
        print("helo")
        print(request)
        print(response)
        assert response.status_code == 200
        # assert 1 == 2
        
    def test_2(self):
        self.factory = RequestFactory()
        path = reverse('register')
        request = self.factory.post('/admin')
        response = resolve(path).func(request)
        assert resolve(path).view_name == "register"
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_3(self):
        Account.objects.create(email="user@gmail.com", username="user", password="123")
        me = Account.objects.get(email='user@gmail.com')
        assert me.is_superuser is False
        assert me.has_perm("") is False
        assert me.has_perm("main.change_appointment") is True
        assert str(me) == "user@gmail.com"
        Account.objects.create_superuser(email="user1@gmail.com", username="user", password="123")
        me = Account.objects.get(email='user1@gmail.com')
        assert str(me) == 'user1@gmail.com'
        assert me.has_perm("") is True

    @pytest.mark.django_db
    def test_4(self):
        form = RegistrationForm()
        form.cleaned_data = {"username": "user@gmail.com", "password1": "123", "password2": "124"}
        form.save()
        assert len(Account.objects.all()) == 1




