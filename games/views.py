from platform import release
from django.shortcuts import render
from django.db.models import Avg
from babel.dates import format_date
from .models import Rating,Game
from .yt_id_parser import get_yt_id

# Create your views here.

def game_site(request, id):
    game = Game.objects.get(pk=id)
    ratings = Rating.objects.filter(game = game)

    if ratings:
        avg = ratings.aggregate(Avg("stars"))
    else:
        avg = None
    
    if game.trailer:
        trailer_id = get_yt_id(game.trailer)
    else:
        trailer_id = None

    context = {'game': game, 'ratings': ratings, 'avg': avg, 'release_date': format_date(game.release_date, locale="pl_PL"), 'trailer_id': trailer_id}
    return render(request, "games/game_template.html", context)