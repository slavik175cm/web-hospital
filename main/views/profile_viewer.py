from .views import my_render
from authentication.models import Account as User
from main.models import Patient
from main.forms import ProfileForm


@my_render('profile.html')
def profile_viewer(request, user_id):
    user = User.objects.get(pk=user_id)
    if not request.user.is_authenticated:
        error_message = 'авторизуйтесь для промотра этой страницы'
        return {"error_message": error_message}
    if not request.user == user:
        error_message = 'нельзя изменять не свои данные:)'
        return {"error_message": error_message}
    patient = Patient.objects.get(user=user)
    if request.method == "POST":
        form = ProfileForm(request.POST)
        data = query_dict_to_dict(form.data)
        print(data)
        password_error = ''
        password1_error = ''
        password2_error = ''

        success_message = ''
        print(user.password)
        if data['password'] == '':
            password_error = 'Обязательное поле'
        elif not user.check_password(data['password']):
            password_error = 'Неверный пароль'

        if data['new_password1'] != data['new_password2']:
            password1_error = 'пароли не совпадают'
            password2_error = 'пароли не совпадают'
        print("asa", form.is_valid())
        print(**get_errors_from_query_dict(form.errors))
        print(password_error)
        if form.is_valid() and password_error == ''\
                and password1_error == '' and password2_error == '':
            if data['new_password1'] != '':
                user.set_password(data['new_password1'])
                user.save()
            # patient = form.save(commit=False)
            # patient.user = user
            # patient.save()
            updated_patient = form.save(commit=False)
            # for field in Patient._meta.get_fields()[1:]:
            #     patient.__setattr__(str(field), updated_patient.__getattribute__(str(field)))
            patient.first_name = updated_patient.first_name
            patient.middle_name = updated_patient.middle_name
            patient.last_name = updated_patient.last_name
            patient.birth_date = updated_patient.birth_date
            patient.address = updated_patient.address
            patient.phone_number = updated_patient.phone_number

            patient.save()

            success_message = 'Данные успешно сохранены'
        return {**data, **get_errors_from_query_dict(form.errors),
                "success_message": success_message, "password_error": password_error,
                "new_password1_error": password1_error, "new_password2_error": password2_error}

    return {"first_name": patient.first_name, "middle_name": patient.middle_name,
            "last_name": patient.last_name, "phone_number": patient.phone_number,
            "address": patient.address, "birth_date": str(patient.birth_date)}


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
