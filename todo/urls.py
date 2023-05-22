from django.urls import path, include
from homepage_app.views import home_page
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_app.urls')),
    path('todo/', include('todo_app.urls')),
    path('transcribe/', include('transcribe_app.urls')),
    path('cases/', include('cases_app.urls')),
    path('snake/', include('snake_app.urls')),
    path('accounts/', include('allauth.urls')),
    path('converter/', include('converter_app.urls')),
    path('', home_page, name='home_page')
]
