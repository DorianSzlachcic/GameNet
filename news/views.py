from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from babel.dates import format_datetime

from .models import News
from .forms import NewsForm
from .decorators import check_if_redactor

# Create your views here.

def news_site(request, id):
    news_object = News.objects.get(pk=id)

    context = {'news': news_object}
    return render(request, "news/news_site.html", context)

def news_list(request):
    page = request.GET.get('page',1)

    paginator = Paginator(News.objects.all().order_by("-edit_date"), 10)

    try:
        news_objects = paginator.get_page(page)
    except PageNotAnInteger:
        news_objects = paginator.get_page(1)
    except EmptyPage:
        news_objects = paginator.page(paginator.num_pages)

    context = {'news_objects': news_objects}
    return render(request, "news/news_list.html",context)

@login_required
def your_news(request):
    user = request.user
    check_if_redactor(user)

    user_news = News.objects.filter(author=user).order_by('-edit_date')

    last_edited = []
    for last in user_news.values_list("edit_date",flat=True):
        last_edited.append(format_datetime(last, locale="pl_PL"))

    context = {'user_news': zip(user_news, last_edited) if user_news.count() != 0 else None}
    return render(request, "news/your_news.html", context)

@login_required
def add(request):
    check_if_redactor(request.user)

    form = NewsForm()

    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return redirect('yourNews')

    context = {'form': form}
    return render(request, "news/add_edit.html", context)


@login_required
def edit(request, id):
    check_if_redactor(request.user)

    news = News.objects.get(pk=id)
    form = NewsForm(instance=news)

    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return redirect('yourNews')

    context = {'form': form, 'edit': True}
    return render(request, "news/add_edit.html", context)


@login_required
def delete(request, id):
    check_if_redactor(request.user)

    if request.method == "POST":
        news = News.objects.get(pk=id)
        news.delete()
        return redirect("yourNews")
    return render(request, "news/confirm_delete.html")
