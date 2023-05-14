from django.urls import path, include
from todo_app.views import home_page

urlpatterns = [
    path('auth/', include('auth_app.urls')),
    path('todo/', include('todo_app.urls')),
    path('transcribe/', include('transcribe_app.urls')),
    path('cases/', include('homework_app.urls')),
    path('', home_page, name='home_page')
]
