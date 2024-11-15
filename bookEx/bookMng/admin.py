from django.contrib import admin


# Register your models here.

from bookMng.models import MainMenu
from bookMng.models import Book

admin.site.register(MainMenu)
admin.site.register(Book)
