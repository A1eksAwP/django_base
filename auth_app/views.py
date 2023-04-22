from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.contrib import auth
from django.contrib.auth.models import User
from auth_app.service.validator.Validator import RegisterValidator
from auth_app.service.validator.exceptions.ValidateExceprion import ValidateException


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
        # Область подключенных сервисов
        request_data = request.POST.dict()
        try:
            RegisterValidator(request_data).validate()
        except ValidateException as exception:
            return render(request, 'error_page.html', {
                'errors': exception.error_list
            })

        # Область определения
        username = request_data['username']
        password = request_data['password']
        password_confirm = request_data['password_conf']
        email = request_data['email']
        name = request_data['name']
        phone_number = request_data['phone']

        # Область логики
        # TODO Создать пользователя

        # Область результата
        return render(request, 'info.html', {
            'message': f'Пользователь {username} успешно зарегистрирован в системе!'
        })
    return render(request, 'register.html')


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
