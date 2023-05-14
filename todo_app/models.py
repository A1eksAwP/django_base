from django.contrib.auth.models import User
from django.db import models


class TodoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()


class TodoStatus(models.Model):
    COMPLETED = 1
    NOT_COMPLETED = 2
    OVERDUE = 3
    CANCELED = 4
    name = models.TextField()


class TodoTask(models.Model):
    todo_list = models.ForeignKey(TodoList, models.CASCADE)
    create_at = models.DateTimeField()
    complete_at = models.DateTimeField(null=True)
    status = models.ForeignKey(TodoStatus, models.CASCADE)
    title = models.TextField()
    text = models.TextField()
    by_user = models.TextField(null=True)
