from multiprocessing import context
from operator import itemgetter
import django
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from babel.dates import format_datetime


from games.models import Rating, Game
from news.models import News
from .forms import RegisterForm
from accounts.tokens import TokenGenerator

# Create your views here.

def homePage(request):

    news3 = News.objects.order_by("-edit_date")

    top5 = []
    for game in Game.objects.all():
        ratings = Rating.objects.filter(game=game)
        if ratings:
            avg = ratings.aggregate(Avg('stars'))['stars__avg']
            top5.append((game, avg))
    
    top5 = sorted(top5, key=itemgetter(1),reverse=True)[:5]

    while len(top5) < 5:
        top5.append((None,None))

    context = {'top5': top5, 'news3': news3}
    return render(request, "home.html", context)



def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = AuthenticationForm()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Nie udało się zalogować użytkownika.",extra_tags="danger")

    context = {'form': form}
    return render(request, "accounts/login.html", context)



def logoutUser(request):
    logout(request)
    messages.success(request,"Wylogowano pomyślnie.",extra_tags="success")
    return redirect('login')




def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
    
        form.fields['email'].required = True

        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            token_generator = TokenGenerator()
            message_txt = render_to_string('accounts/activation_email.txt', {
                'user': user,
                'domain': get_current_site(request).domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token_generator.make_token(user),
            })

            message_html = render_to_string('accounts/activation_email.html', {
                'user': user,
                'domain': get_current_site(request).domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token_generator.make_token(user),
            })

            send_mail("Link aktywacyjny - GameNet", 
                message_txt, 
                settings.EMAIL_HOST_USER, 
                [form.cleaned_data.get('email')],
                fail_silently=False, 
                html_message=message_html
            )

            messages.success(request, "Na podanego maila został wysłany link aktywacyjny. Przed zalogowaniem prosze aktywować konto.", extra_tags="success")
            return redirect('login')

    context = {'form': form}
    return render(request, "accounts/register.html", context)


@login_required
def profilePage(request):

    user_ratings = Rating.objects.filter(author=request.user).order_by("-edit_date")
    
    last_edit_dates = user_ratings.values_list("edit_date",flat=True)
    last_edit_formated = []

    for last in last_edit_dates:
        last_edit_formated.append(format_datetime(last, locale="pl_PL"))

    context = {'user_ratings': zip(user_ratings,last_edit_formated) if user_ratings else None }
    return render(request, "accounts/my_profile.html", context)

@login_required
def change_password(request):

    form = PasswordChangeForm(request.user)

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Hasło zostało zmienione", extra_tags="success")
            return redirect('changePassword')

    context = {'form': form }
    return render(request, "accounts/change_password.html", context)

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    token_generator = TokenGenerator()
    if user != None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        messages.error(request,"Nie udało się aktywować konta.",extra_tags="danger")
        return redirect('login')

@login_required
def deleteAccount(request):
    if request.method == "POST":
        account = request.user

        logout(request)
        account.delete()

        messages.error(request,"Usunięto konto",extra_tags="danger")
        return redirect('login')
    else:
        return render(request, "accounts/confirm_delete_acc.html")