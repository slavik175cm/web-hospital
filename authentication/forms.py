from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account as User
from main.models import Patient


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=30)

    class Meta:
        model = User
        fields = ["email", 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
        return user


class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["first_name", "middle_name", "last_name",
                  "phone_number", "birth_date", "address"]
