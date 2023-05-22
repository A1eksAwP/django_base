from django.core.management import BaseCommand
from converter_app.models import Converter, Currency, Settings
from credentials import currency_api_key as api_key
import json
import requests


class Command(BaseCommand):
    help = 'Сбор и обновление данных о курсе валют с сайта'

    def handle(self, *args, **options):
        base_currency = 'RUB'
        api_url = f'https://api.currencyapi.com/v3/latest?apikey={api_key}&base_currency={base_currency}'
        response = requests.get(api_url)
        currency_rates = json.loads(response.content)
        all_currency = {cur_id: cur_data['value'] for cur_id, cur_data in currency_rates['data'].items()}
        new_count, update_count = 0, 0
        for cur_id, cur_value in all_currency.items():
            if not Currency.objects.filter(id=cur_id).exists() and len(cur_id) <= 3:
                Currency(id=cur_id, value=cur_value).save()
                new_count += 1
            db_cur: Currency = Currency.objects.filter(id=cur_id).first()
            if db_cur and db_cur.value != cur_value and len(cur_id) <= 3:
                db_cur.value = cur_value
                db_cur.save()
                update_count += 1
        print(f"Все ОК! Добавлено: {new_count} объектов; Обновлено цен: {update_count}")
