from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import Account as User
from main.models import Patient


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=30)
    # first_name = forms.CharField(max_length=30)
    # second_name = forms.CharField(max_length=30)
    # last_name = forms.CharField(max_length=30)
    # phone_number = forms.CharField(max_length=30)
    # birth_date = forms.DateField()

    class Meta:
        model = User
        # fields = ["username", "first_name", "second_name",
        #           "phone_number", "birth_date", "last_name", "password1", "password2"]
        fields = ["email", 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)

        # user.first_name = self.cleaned_data['first_name']
        # user.second_name = self.cleaned_data['second_name']
        # user.last_name = self.cleaned_data['last_name']
        # user.phone_number = self.cleaned_data['phone_number']
        # user.birth_date = self.cleaned_data['birth_date']

        if commit:
            user.save()
        return user


class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["first_name", "last_name",
                  "phone_number", "birth_date", "last_name", "address"]
