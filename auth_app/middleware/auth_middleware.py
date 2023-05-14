from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect
from django.urls import reverse


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest):
        unlogin_views = (reverse('login'), reverse('register'))
        if not request.user.is_authenticated and request.path not in unlogin_views:
            path = request.build_absolute_uri()
            login_url = reverse('login')
            return redirect(f'{login_url}?next_page={path}')
        return self.get_response(request)
