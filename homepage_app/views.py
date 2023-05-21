from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render


APPS = {
    'AuthApp': {
        'url': 'auth/login',
        'description': 'Приложение для создания и валидации пользователей на сайте'
    },
    'ToDo': {
        'url': 'todo/',
        'description': 'Здесь можно писать задачи, или задавать задачи определенному пользователю'
    },
    'Transcribe': {
        'url': 'transcribe/',
        'description': 'Позволяет через ссылку на YouTube плейлист или видео распарсить оттуда все \
    транскрипции и запускать встроенный плеер для мгновенного перехода по таймкодам'
    },
    'ChangeCase': {
        'url': 'cases/',
        'description': 'Здесь можно поменять стиль текста выбрав один из вариантов (стилей) написания'
    },
    'SnakeGame': {
        'url': 'snake/',
        'description': 'Игра "Змейка", с различными уровнями сложности и таблицей рекордов пользователей'
    },
    'UserList': {
        'url': 'auth/user_list',
        'description': 'Здесь можно управлять пользователями, но только если вы администратор, разумеется'
    },
    'HomePage': {
        'url': '',
        'description': 'Приложение, поясняющее собой все остальные приложения на сайте'
    },
}


def home_page(request: WSGIRequest):
    return render(request, 'home_page.html', {
        'apps_dict': APPS,
    })
