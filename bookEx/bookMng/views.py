from functools import wraps, reduce

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.utils.functional import SimpleLazyObject

from django.contrib.auth import get_user_model

from .models import Book, MainMenu, Rating, Comment, Favorite
from bookMng.forms import CommentForm
from bookMng.forms import BookForm


User = get_user_model()

def verify_user_id(view_func):
    # Wrapper for checking if user is logged in before calling APIs below.
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user_id = request.user.id if request.user.is_authenticated else -1
        if user_id == -1:
            return JsonResponse({"status": "failed. User not logged in"})
        request.user_id = user_id
        return view_func(request, *args, **kwargs)
    return wrapper


@verify_user_id
def postbook(request):
    submitted = False
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect("/postbook?submitted=True")
    else:
        form = BookForm()
        if "submitted" in request.GET:
            submitted = True
    return render(
        request,
        "bookMng/postbook.html",
        {"form": form, "submitted": submitted},
    )

def displaybook(request):
    books = Book.objects.all()
    user_id = request.user.id if request.user.is_authenticated else -1

    return render(
        request,
        "bookMng/displaybooks.html",
        {
            "books": books,
            "user_id": user_id
        },
    )

@verify_user_id
def mybooks(request):
    user_id = request.user_id
    books = Book.objects.filter(username=request.user)

    return render(
        request,
        "bookMng/displaybooks.html",
        {
            "myBook": 1,
            "books": books,
            "user_id": user_id
        },
    )

def displayUser(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"status": "failed. User does not exist"})

    books = Book.objects.filter(username=user)

    return render(
        request,
        "bookMng/displaybooks.html",
        {
            "books": books,
            "user_id": user_id
        },
    )

@verify_user_id
def favoriteBooks(request):
    favoriteBooks = Favorite.objects.filter(user=request.user)
    favoriteBooks = [favoriteBook.book for favoriteBook in favoriteBooks]

    return render(
        request,
        "bookMng/displaybooks.html",
        {
            "books": favoriteBooks,
            "user_id": request.user.id
        },
    )

def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    book.pic_path = book.picture.url[14:]

    comments = Comment.objects.filter(book=book)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            try:
                comment.book = book_id
                comment.user = request.user
            except Exception:
                pass
            comment.save()

    return render(
        request,
        "bookMng/book_detail.html",
        {
            "book": book,
            "comments": comments,
        },
    )

def search(request):
    user_id = request.user.id if request.user.is_authenticated else -1
    searchbar = request.POST['searchbar']
    searchbooks = Book.objects.filter(name__contains=searchbar)
    return render(
        request,
        "bookMng/displaybooks.html",
        {
            "searchbar": searchbar,
            "books": searchbooks,
            "user_id": user_id,
        })

def aboutus(request):
    return render(
        request,
        "bookMng/aboutus.html",
    )


def deletebook(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()

    return render(
        request,
        "bookMng/deletebook.html",
        )


def likeBook(rating: int, book: Book, user):
    Rating.objects.create(rating=rating, book=book, user=user)


class Register(CreateView):
    template_name = "registration/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("register-success")

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)


# Utilities
@verify_user_id
def getFavoriteBooks(request):
    # Returns an array of favorite books ids if the user is logged in.
    user_id = request.user_id
    
    favorites = Favorite.objects.filter(user_id=user_id).values("book_id")
    book_ids = [favorite["book_id"] for favorite in favorites.values()]
    data = {
        "data": book_ids
    }

    return JsonResponse(data)

@verify_user_id
def toggleFavoritesByBookID(request, book_id):
    user_id = request.user_id

    favoriteBooks = Favorite.objects.filter(user_id=user_id, book_id=book_id)
    if len(favoriteBooks) > 0:
        favoriteBook = favoriteBooks[0]
        favoriteBook.delete()
    else:
        book = Book.objects.get(id=book_id)
        Favorite.objects.create(book=book, user=request.user)


    data = {
        "book_id": book_id,
        "status": "success"
    }
    return JsonResponse(data)

@verify_user_id
def getRatingByBookID(request, book_id):
    user_id = request.user_id

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return JsonResponse({
            "rating": 0,
            "status": "failed. No rating available for this book or from this user."
        })

    ratings = Rating.objects.filter(book=book, user=request.user)
    if len(ratings) == 0:
        return JsonResponse({
            "rating": 0,
            "status": "failed. No rating available for this book or from this user."
        })

    data = {
        "rating": ratings[0].rating,
        "status": "success"
    }
    return JsonResponse(data)

def getAverageRatingByBookID(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return JsonResponse({"status": "failed. No rating available for this book or from this user."})

    ratings = Rating.objects.filter(book=book)
    if len(ratings) == 0:
        return JsonResponse({
            "avgRating": 0,
            "status": "failed. No rating available for this book or from this user."
        })
    elif len(ratings) == 1:
        sum_of_ratings = ratings[0].rating
    else:
        # sum_of_ratings = reduce(lambda a,b: a.rating + b.rating, ratings)
        sum_of_ratings = 0
        for rating in ratings:
            sum_of_ratings += rating.rating
    total_raters = len(ratings)
    avgRating = round(sum_of_ratings / total_raters, 2)

    data = {
        "avgRating": avgRating,
        "totalRaters": total_raters,
        "status": "success"
    }
    return JsonResponse(data)

@verify_user_id
def addCommentByBookID(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return JsonResponse({"status": "failed. No rating available for this book or from this user."})

    comment = request.GET.get("comment")

    Comment.objects.create(comment=comment, book=book, user=request.user)

    return JsonResponse({"status": "success"})


@verify_user_id
def rateByBookID(request, book_id):
    user_id = request.user_id
    rating_value = request.GET.get("rating")
    
    try:
        rating_value = int(rating_value)
        if rating_value <= 0 or rating_value > 5:
            return JsonResponse({"status": "failed. Rating query can not be less than 1 or greater than 5."})
    except TypeError:
        return JsonResponse({ "status": "failed. Ratings query can not be parsed into integer."})

    ratings = Rating.objects.filter(user_id=user_id, book_id=book_id)

    if len(ratings) == 0:
        book = Book.objects.get(id=book_id)
        Rating.objects.create(rating=rating_value, book=book, user=request.user)
    else:
        rating = ratings[0]
        rating.rating = rating_value
        rating.save()
    data = {
        "book_id": book_id,
        "rating": rating_value,
        "status": "success"
    }
    return JsonResponse(data)