from django.forms import ModelForm
from bookMng.models import Book


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            "name",
            "web",
            "price",
            "picture",
        ]
