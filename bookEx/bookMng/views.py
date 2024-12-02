from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.utils.functional import SimpleLazyObject

from bookMng.forms import BookForm
from bookMng.forms import CommentForm
from .models import Book, MainMenu, Rating, Comment


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

# def postcomment(request):
#     submitted = False
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             try:
#                 comment.book = request.bookid
#                 comment.user = request.user
#             except Exception:
#                 pass
#             comment.save()
#     else:
#         form = CommentForm()
#         if "submitted" in request.GET:
#             submitted = True
#     return render(
#         request,
#         "bookMng/book_detail.html",
#         {"form": form, "submitted": submitted},)

def displaybook(request):
    books = Book.objects.all()

    return render(
        request,
        "bookMng/displaybooks.html",
        {
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

    comments = Comment.objects.all()

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
