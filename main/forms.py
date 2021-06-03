from django import forms
from authentication.models import Account as User
from main.models import Patient
from django.db import models


class ProfileForm(forms.ModelForm):
    password = models.CharField('password', max_length=128)
    new_password1 = models.CharField('new_password1', max_length=128)
    new_password2 = models.CharField('new_password2', max_length=128)

    class Meta:
        model = Patient
        fields = ["first_name", "middle_name", "last_name",
                  "phone_number", "birth_date", "address"]
