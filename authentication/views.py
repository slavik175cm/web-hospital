from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm, PatientRegistrationForm
from django.contrib import messages


def register_viewer(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        patient_form = PatientRegistrationForm(request.POST)
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password1')

        address = request.POST.get('address')
        print(password1)
        print(address)

        if form.is_valid() and patient_form.is_valid():
            user = form.save()

            patient = patient_form.save(commit=False)
            patient.user = user

            patient.save()
            # phone_number = request.POST.get('phone_number')
            # username = request.POST.get('username')
            email = request.POST.get('email')

            password = request.POST.get('password1')
            # print(phone_number)
            print(email)
            print(password)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                print("yoooo")
                return redirect('/info')
        else:
            print("form is invalid")
            for msg in form.errors.as_data():
                print(msg)
                if msg == 'email':
                    print("1!")
                if msg == 'password2' and password1 == password2:
                    print("2!")
                elif msg == 'password2' and password1 != password2:
                    print("3!")
        return render(request, 'register.html', {"form": form})
    else:
        return render(request, 'register.html', {})


def login_viewer(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/info')
        else:
            messages.info(request, 'something is wrong')
            return render(request, 'login.html', {})
    # messages.info(request, 'hey there')
    return render(request, 'login.html', {})


def logout_viewer(request):
    logout(request)
    return redirect('login')
