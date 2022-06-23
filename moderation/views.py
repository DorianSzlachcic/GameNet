from django.shortcuts import render, redirect
from babel.dates import format_datetime

from games.models import Rating
from .models import ModerationMessage

# Create your views here.

def moderator_panel(request):
    to_moderate = Rating.objects.filter(accepted = None).order_by("edit_date")

    created_dates = to_moderate.values_list("created_date",flat=True)
    created_formated = []

    for date in created_dates:
        created_formated.append(format_datetime(date, locale="pl_PL"))

    context = {'to_moderate': zip(to_moderate, created_formated) if to_moderate.count() != 0 else None}
    return render(request, "moderation/moderator_panel.html", context)

def accept(request, id):
    rating = Rating.objects.get(pk = id)
    if rating.accepted == None:
        rating.accepted = True
        rating.save()
    
    message = ModerationMessage(rating = rating, accepted = True)
    message.save()

    return redirect('moderatorPanel')

def reject(request, id):
    rating = Rating.objects.get(pk = id)
    if rating.accepted == None:
        rating.accepted = False
        rating.save()

    message = ModerationMessage(rating = rating, accepted = False)
    message.save()

    return redirect('moderatorPanel')