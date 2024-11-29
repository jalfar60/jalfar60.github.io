from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.utils.functional import SimpleLazyObject

from bookMng.forms import BookForm
from .models import Book, MainMenu, Rating, Comment, Favorite


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
    user_id = request.user.id

    favorites = Favorite.objects.values_list("book_id", flat=True).filter(user_id=user_id)
    
    print(favorites)
    print(books.values())
    for book in books:
        setattr(book, "is_favorite", book.id in favorites)


    return render(
        request,
        "bookMng/displaybooks.html",
        {
            "books": books,
            "favorites": favorites
        },
    )


def mybooks(request):
    books = Book.objects.filter(username=request.user)

    for b in books:
        b.pic_path = b.picture.url[14:]

    return render(
        request,
        "bookMng/mybooks.html",
        {
            "books": books,
        },
    )


def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    # likeBook(2, book=book, user=request.user)
    book.pic_path = book.picture.url[14:]
    # print(type(book))
    # ratings = list(map(lambda a: a.rating, book.ratings.all()))
    # print(ratings)

    return render(
        request,
        "bookMng/book_detail.html",
        {
            "book": book,
        },
    )


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

# Utilities
def getFavoritesByUserID(request, user_id: int):
    # Returns an array of favorite books ids given the user_id.
    favorites = Favorite.objects.filter(user_id=user_id)
    book_ids = [favorite["book_id"] for favorite in favorites.values()]
    data = {
        "data": book_ids
    }
    print(data)
    return JsonResponse(data)


class Register(CreateView):
    template_name = "registration/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("register-success")

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)
