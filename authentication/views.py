from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, PatientRegistrationForm
from django.contrib import messages
from django.urls import reverse
from HospitalDjango import settings

from django.core.mail import EmailMessage
from .token_generator import token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import threading


def make_new_thread(func, *args, **kwargs):
    new_thread = threading.Thread(target=func, args=args, kwargs=kwargs)
    new_thread.start()


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
            # user = authenticate(request, email=email, password=password)
            if user is not None:
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64': uidb64,
                                                   'token': token_generator.make_token(user)})
                activate_url = 'http://' + domain + link

                email_body = "Перейдите по адресу \n" + activate_url + ' для подтверждения электронного адреса\n'

                email_subject = 'Активацияя аккаунта поликлиники.'
                email = EmailMessage(email_subject, email_body, settings.EMAIL_HOST_USER, to=[email])

                make_new_thread(email.send, fail_silently=False)
                messages.success(request, 'подтвердите почту для авторизации')

                return redirect('/login')
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
        if user is None:
            messages.info(request, 'почта и/или пароль некорректны')
            return render(request, 'login.html', {'username': username, 'password': password})
        elif not user.is_email_verified:
            messages.info(request, 'подтвердите почту для авторизации')
            return render(request, 'login.html', {'username': username, 'password': password})
        login(request, user)
        return redirect('/info')

    return render(request, 'login.html', {})


def logout_viewer(request):
    logout(request)
    return redirect('login')


from django import views
from .models import Account as User


class VerificationView(views.View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.refresh_from_db()
            user.is_email_verified = True

            user.save()
            messages.info(request, 'Ваш аккаунт был успешно активирован!')
            return redirect('/login')
        else:
            messages.info(request, f'Активационная ссылка некоррекна или уже была использована')
            return redirect('/login')
