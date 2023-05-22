from django.urls import path
from converter_app.controllers.views import converter_index, convert

urlpatterns = [
    path('', converter_index, name='converter_view'),
    path('convert/', convert, name='convert_view')
]