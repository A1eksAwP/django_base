from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.contrib import auth
from django.contrib.auth.models import User
from .utils.validators import validate_username, validate_name, validate_password, validate_email, validate_phone, \
    bad_phone, not_equal_passwords, bad_username, bad_password, bad_email, bad_name, user_already_exist
from django.http import HttpResponseNotModified


def login(request: WSGIRequest):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user: User = auth.authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'login.html', {
                'error': 'Неверный логин или пароль',
            })
        if user.is_active:
            auth.login(request, user)
            return redirect('main')
    return render(request, 'login.html')


def register(request: WSGIRequest):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_conf')
        email = request.POST.get('email')
        name = request.POST.get('name')
        phone_number = request.POST.get('phone')
        params = (username, password, password_confirm, email, name, phone_number)
        errors = validate_register(*params)
        if errors:
            return render(request, 'register.html', {
                'errors': errors
            })
        errors = save_new_user(*params)
        return render(request, 'info.html', {
            'errors': errors,
            'message': f'Пользователь {username} успешно зарегистрирован в системе!'
        })
    return render(request, 'register.html')


def validate_register(username, password, password_confirm,
                      email, name, phone_number) -> list[str]:
    errors = []
    if User.objects.filter(username=username).exists():
        errors.append(user_already_exist)
    if User.objects.filter(email=email).exists():
        errors.append(user_already_exist)
    if password != password_confirm:
        errors.append(not_equal_passwords)
    if not validate_username(username) or len(username) < 6:
        errors.append(bad_username)
    if not validate_password(password):
        errors.append(bad_password)
    if not validate_email(email):
        errors.append(bad_email)
    if not validate_name(name):
        errors.append(bad_name)
    if not validate_phone(phone_number):
        errors.append(bad_phone)
    return errors


def save_new_user(username, password, password_confirm,
                  email, name, phone_number) -> list[str]:
    errors = []
    new_user = User()
    new_user.username = username
    new_user.set_password(password)
    new_user.email = email
    new_user.name = name
    new_user.phone = phone_number
    try:
        new_user.save()
    except Exception as e:
        errors.append(f'Создать пользователя {username} не удалось. Ошибка сервера: {e}')
    return errors


def logout(request: WSGIRequest):
    auth.logout(request)
    # return HttpResponseNotModified() -> Так можно сделать статус 304
    return redirect('login')


def edit(request: WSGIRequest):
    return render(request, 'edit.html')


def user_list(request: WSGIRequest):
    if request.user.is_superuser:
        users = User.objects.all()
        return render(request, 'user_list.html', {
            'users': users
        })
    return render(request, 'info.html', {
        'message': 'У вас недостаточно прав на просмотр этой страницы.'
    })


def filter_users(request: WSGIRequest):
    if request.user.is_superuser:
        query = request.POST.get('filter')
        users = User.objects.filter(username__icontains=query).all()
        return render(request, 'user_list.html', {
            'users': users
        })
    return render(request, 'info.html', {
        'message': 'У вас недостаточно прав на просмотр этой страницы.'
    })


def quick_login(request: WSGIRequest):
    user_id = request.POST.get('user_id')
    user = User.objects.get(pk=user_id)
    auth.login(request, user)
    return redirect('main')


def ask(request: WSGIRequest):
    user_id = request.POST.get('delete_id')
    user = User.objects.get(pk=user_id)
    return render(request, 'info.html', {
        'message': f'Удалить пользователя {user.username}?',
        'delete_id': user_id
    })


def delete(request: WSGIRequest):
    user_id = request.POST.get('delete_id')
    user = User.objects.get(pk=user_id)
    if user.is_superuser:
        return render(request, 'info.html', {
            'message': f'Администраторов удалять нельзя. {user.username}',
        })
    if user:
        user.is_active = False
        user.save()
    return redirect('user_list')
