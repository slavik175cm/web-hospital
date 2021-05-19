from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, PatientRegistrationForm
from django.contrib import messages


def register_viewer(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        patient_form = PatientRegistrationForm(request.POST)
        if form.is_valid() and patient_form.is_valid():
            user = form.save()

            patient = patient_form.save(commit=False)
            patient.user = user

            patient.save()
            email = request.POST.get('email')

            password = request.POST.get('password1')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/info')
        return render(request, 'register.html', {**{"form": form}, **query_dict_to_dict(form.data),
                                                 **get_errors_from_query_dict(form.errors.items()),
                                                 **get_errors_from_query_dict(patient_form.errors.items())})
    else:
        return render(request, 'register.html', {})


def query_dict_to_dict(data):
    data = dict(data)
    for item in data:
        data[item] = str(data[item])[2:-2]
    return data


def get_errors_from_query_dict(data):
    data = dict(data)
    response = {}
    for key, value in data.items():
        response[key + "_error"] = str(value)[26:-10]
    return response


def login_viewer(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/info')
        else:
            messages.info(request, 'почта и/или пароль некорректны')
            return render(request, 'login.html', {'username': username, 'password': password})
    return render(request, 'login.html', {})


def logout_viewer(request):
    logout(request)
    return redirect('login')
