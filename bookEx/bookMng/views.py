from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.utils.functional import SimpleLazyObject

from bookMng.forms import BookForm
from .models import Book, MainMenu, Rating


def index(request):
    return render(request, "bookMng/index.html", {"item_list": MainMenu.objects.all()})


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
        {"form": form, "item_list": MainMenu.objects.all(), "submitted": submitted},
    )


def displaybook(request):
    books = Book.objects.all()

    return render(
        request,
        "bookMng/displaybooks.html",
        {
            "item_list": MainMenu.objects.all(),
            "books": books,
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
            "item_list": MainMenu.objects.all(),
            "books": books,
        },
    )


def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    # likeBook(2, book=book, user=request.user)
    # book.pic_path = book.picture.url[14:]
    # print(type(book))
    # ratings = list(map(lambda a: a.rating, book.ratings.all()))
    # print(ratings)

    return render(
        request,
        "bookMng/book_detail.html",
        {
            "item_list": MainMenu.objects.all(),
            "book": book,
        },
    )


def aboutus(request):
    return render(
        request, "bookMng/aboutus.html", {"item_list": MainMenu.objects.all()}
    )


def deletebook(request, book_id):

    book = Book.objects.get(id=book_id)
    book.delete()

    return render(
        request,
        "bookMng/deletebook.html",
        {
            "item_list": MainMenu.objects.all(),
        },
    )


def likeBook(rating, book, user):
    Rating.objects.create(rating=rating, book=book, user=user)


class Register(CreateView):
    template_name = "registration/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("register-success")

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)
