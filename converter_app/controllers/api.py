from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
import django.core.exceptions as ex

from converter_app.models import Currency


def converter_index(request: WSGIRequest):
    return JsonResponse({"message": "Hello converter!"})


def convert(request: WSGIRequest):
    request_data = {
        "from": request.GET.get('from', False),
        "count": request.GET.get('count', False),
        "to": request.GET.get('to', False),
    }
    __validate_fields(request_data)
    currency_from = Currency.objects.get(pk=request_data['from'])
    currency_to = Currency.objects.get(pk=request_data['to'])
    count = float(request_data['count'])
    result: float = currency_to.value / currency_from.value * count

    return JsonResponse({
        "from": currency_from.id,
        "count": count,
        "to": currency_to.id,
        "result": result,
    })


def __validate_fields(data: dict):
    if [x for x in data.values() if not x]:
        raise ex.ValidationError('Не все обязательные поля заполнены.', 422)
