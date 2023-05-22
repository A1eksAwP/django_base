from django.db import models
from django.contrib.auth.models import AbstractUser


# ToDo нужно разобраться с ошибками при миграциях и добавить поле "телефон"
# class MyUser(AbstractUser):
#     phone = models.IntegerField(verbose_name='phone', unique=True)
