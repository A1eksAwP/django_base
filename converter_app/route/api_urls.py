from django.urls import path
from converter_app.controllers.api import converter_index, convert

urlpatterns = [
    path('', converter_index, name='converter_api'),
    path('convert/', convert, name='convert'),
]