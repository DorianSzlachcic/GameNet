from email.utils import format_datetime
from platform import release
from django.shortcuts import redirect, render
from django.db.models import Avg
from django.contrib.auth.decorators import login_required

from babel.dates import format_date, format_datetime
from .models import Rating,Game
from .yt_id_parser import get_yt_id
from .forms import RatingForm

# Create your views here.

def game_site(request, id):
    game = Game.objects.get(pk=id)
    
    if game.trailer:
        trailer_id = get_yt_id(game.trailer)
    else:
        trailer_id = None
    
    form = RatingForm()

    if request.method == "POST":
        form = RatingForm(request.POST)

        if form.is_valid():
            rating = form.save(commit=False)
            rating.author = request.user
            rating.game = game
            rating.save()
            form = RatingForm()



    ratings = Rating.objects.filter(game = game)

    if ratings:
        avg = ratings.aggregate(Avg("stars"))
    else:
        avg = None

    last_edit_dates = Rating.objects.filter(game = game).values_list("edit_date",flat=True)
    last_edit_formated = []

    for last in last_edit_dates:
        last_edit_formated.append(format_datetime(last, locale="pl_PL"))

    context = {
        'game': game, 
        'ratings': zip(ratings,last_edit_formated) if ratings else None, 
        'ratings_count': ratings.count() if ratings else None,
        'avg': avg, 
        'release_date': format_date(game.release_date, locale="pl_PL"), 
        'trailer_id': trailer_id,
        'form': form
    }
    return render(request, "games/game_template.html", context)

@login_required
def deleteRating(request, id):
    rating = Rating.objects.get(pk=id)
    rating.delete()
    return redirect('profile')

@login_required
def editRating(request, id):
    rating = Rating.objects.get(pk=id)

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating.description = form.cleaned_data["description"]
            rating.stars = form.cleaned_data["stars"]
            rating.save()
            return redirect('profile')

    form = RatingForm(instance=rating)

    context = {'form': form, 'game_title': rating.game.title}
    return render(request, "games/edit_rating.html", context)

def search(request):
    if request.method == "POST":
        searched_games = Game.objects.filter(title__contains = request.POST.get('search'))
    context = {'searched_games': searched_games}
    return render(request, "games/search.html",context)