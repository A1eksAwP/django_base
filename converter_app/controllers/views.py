from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect

from converter_app.models import Currency


def converter_index(request: WSGIRequest):
    return render(request, 'converter.html', {
        'all_currency': Currency.objects.all()
    })


def convert(request: WSGIRequest):
    if request.method == 'POST':
        currency_from = Currency.objects.get(pk=request.POST.get('from'))
        currency_to = Currency.objects.get(pk=request.POST['to'])
        count = float(request.POST['count'])
        result: float = currency_to.value / currency_from.value * count
        response_dict = {
            "response_from": currency_from.id,
            "response_count": int(count),
            "response_to": currency_to.id,
            "response_result": f'{result:.4f}',
            'all_currency': Currency.objects.all(),
        }
        return render(request, 'converter.html', response_dict)
    return redirect(converter_index)
