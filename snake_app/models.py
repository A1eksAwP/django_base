from django.contrib.auth.models import User
from django.db import models


class GameDifficulty(models.Model):
    EASY = 1
    MEDIUM = 2
    HARD = 3
    HARDCORE = 4
    level = models.TextField()


# Create your models here.
class PlayerScore(models.Model):
    score = models.BigIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    difficulty = models.ForeignKey(GameDifficulty, models.CASCADE)
    create_at = models.DateField()
