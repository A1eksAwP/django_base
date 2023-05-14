from django.urls import path, include
import homework_app.views as homework

url_case = [
    path('', homework.change_case, name='change_case'),
    path('default_case/', homework.change_case),
    path('sentence_case/', homework.change_case),
    path('upper_case/', homework.change_case),
    path('lower_case/', homework.change_case),
    path('each_word_case/', homework.change_case),
    path('toggle_case/', homework.change_case),
    path('kebab_case/', homework.change_case),
    path('snake_case/', homework.change_case),
    path('camel_case/', homework.change_case),
    path('random_case/', homework.change_case),
    path('rot13_case/', homework.change_case),
    path('cipher_case/', homework.change_case),
]

urlpatterns = [
    path('', include(url_case), name='change_case'),
]
