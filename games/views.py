from email.utils import format_datetime
from platform import release
from django.shortcuts import redirect, render
from django.db.models import Avg, Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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

    ratings = Rating.objects.filter(game = game).filter(accepted = True)

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
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            form.save()
            return redirect('profile')

    form = RatingForm(instance=rating)

    context = {'form': form, 'game_title': rating.game.title}
    return render(request, "games/edit_rating.html", context)

@csrf_exempt
def search(request):
    page = request.GET.get('page', 1)

    if request.GET.get('search'):
        searched_games = Game.objects.filter(Q(title__icontains = request.GET.get('search')) | Q(description__icontains = request.GET.get('search')))
    else:
        searched_games = Game.objects.all()
    
    paginator = Paginator(searched_games, 10)

    try:
        searched_games = paginator.get_page(page)
    except PageNotAnInteger:
        searched_games = paginator.get_page(1)
    except EmptyPage:
        searched_games = paginator.page(paginator.num_pages)

    context = {'searched_games': searched_games}
    return render(request, "games/search.html",context)