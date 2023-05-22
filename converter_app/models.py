from django.db import models


class Converter(models.Model):
    name = models.CharField(max_length=255, null=False)


class Currency(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    value = models.FloatField(null=False)
    updated_at = models.DateTimeField(auto_now=True)


class Settings(models.Model):
    base_currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING)
    converter = models.ForeignKey(Converter, on_delete=models.DO_NOTHING)
