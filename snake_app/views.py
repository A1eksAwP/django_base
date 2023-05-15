from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.contrib.auth.models import User
from snake_app.models import GameDifficulty, PlayerScore
from datetime import datetime


def snake(request: WSGIRequest):
    if request.method == 'POST':
        __set_score(request)
    return render(request, 'snake.html')


def __set_score(request: WSGIRequest):
    score = int(request.POST.get('score'))
    difficulty = int(request.POST.get('difficulty')) + 1
    player = PlayerScore.objects.filter(user=request.user).first()
    if player is None:
        player = PlayerScore(
            user=request.user,
            difficulty=GameDifficulty.objects.get(pk=difficulty),
            create_at=datetime.now()
        )
        player.save()
    last_score = player.score
    if score > last_score:
        player_score = PlayerScore()
        player_score.score = score
        player_score.difficulty = GameDifficulty.objects.get(pk=difficulty)
        player_score.user = User.objects.filter(username=player.user.username).first()
        player_score.create_at = datetime.now()
        player_score.save()


def leaderboards(request):
    LIMIT = 10
    players = PlayerScore.objects.filter(score__gte=1)
    return render(request, 'leaderboards.html', {
        'players': players.order_by('-score')[:LIMIT],
    })
