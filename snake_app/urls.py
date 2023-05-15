from django.urls import path
from snake_app.views import snake, leaderboards


urlpatterns = [
    path('', snake, name='snake'),
    path('leaderboards/', leaderboards, name='leaderboards'),
]
