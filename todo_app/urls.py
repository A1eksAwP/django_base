from django.urls import path
from todo_app.views import todo_main


urlpatterns = [
    path('', todo_main, name='todo'),
]
