from django.forms import ModelForm
from bookMng.models import Book
from bookMng.models import Comment

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            "name",
            "web",
            "price",
            "picture",
        ]

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [
            "comment",
            "book",
            "user",
        ]