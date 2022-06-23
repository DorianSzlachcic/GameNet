from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from babel.dates import format_datetime

from .models import Review
from .forms import ReviewForm
from .decorators import check_if_reviewer

# Create your views here.

def reviews_site(request, id):
    reviews_object = Review.objects.get(pk=id)

    context = {'review': reviews_object}
    return render(request, "reviews/review_site.html", context)

def reviews_list(request):
    page = request.GET.get('page',1)

    paginator = Paginator(Review.objects.all().order_by("-edit_date"), 10)

    try:
        reviews_objects = paginator.get_page(page)
    except PageNotAnInteger:
        reviews_objects = paginator.get_page(1)
    except EmptyPage:
        reviews_objects = paginator.page(paginator.num_pages)

    context = {'reviews_objects': reviews_objects}
    return render(request, "reviews/reviews_list.html",context)

@login_required
def your_reviews(request):
    user = request.user
    check_if_reviewer(user)
    user_reviews = Review.objects.filter(author=user).order_by('-edit_date')

    last_edited = []
    for last in user_reviews.values_list("edit_date",flat=True):
        last_edited.append(format_datetime(last, locale="pl_PL"))

    context = {'user_reviews': zip(user_reviews, last_edited) if user_reviews.count() != 0 else None}
    return render(request, "reviews/your_reviews.html", context)

@login_required
def add(request):
    check_if_reviewer(request.user)

    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            reviews = form.save(commit=False)
            reviews.author = request.user
            reviews.save()
            return redirect('yourReviews')

    context = {'form': form}
    return render(request, "reviews/add_edit.html", context)


@login_required
def edit(request, id):
    check_if_reviewer(request.user)

    review = Review.objects.get(pk=id)
    form = ReviewForm(instance=review)

    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect('yourReviews')

    context = {'form': form, 'edit': True}
    return render(request, "reviews/add_edit.html", context)


@login_required
def delete(request, id):
    check_if_reviewer(request.user)

    if request.method == "POST":
        review = Review.objects.get(pk=id)
        review.delete()
        return redirect("yourReviews")
    return render(request, "reviews/confirm_delete.html")
