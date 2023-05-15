from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from cases_app.utils import SwitchCase


def change_case(request: WSGIRequest):
    case = 'default'
    base_text = ''
    if request.method == 'POST':
        base_text = request.POST.get('text')
        #  требуется проверка, поскольку есть возможность выбора "case" с меню либо url, но url может быть пустым
        if request.POST.get('case') == 'from_url' and not request.path.endswith('change_case/'):
            case = request.path.split('/')[-2].replace('_case', '')
        elif request.POST.get('case') == 'from_url' and request.path.endswith('change_case/'):
            case = 'default'
        else:
            case = request.POST.get('case')
        text = SwitchCase(base_text, case)
    else:
        text = '-'
    return render(
        request,
        'change_case.html',
        {
            'title': 'Case change',
            'base_text': base_text,
            'text': text,
            'case': case
        }
    )
