from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MinValueValidator, MaxValueValidator


class MainMenu(models.Model):
    item = models.CharField(max_length=200, unique=True)
    link = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.item


class Book(models.Model):
    name = models.CharField(max_length=200)
    web = models.URLField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=9)
    publishedate = models.DateField(auto_now=True)
    picture = models.FileField(upload_to="bookEx/static/uploads")
    pic_path = models.CharField(max_length=300, editable=False, blank=True)
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return f"Book) bookname: {self.name}, username: {self.username}"


class Rating(models.Model):
    rating = models.IntegerField(
        blank=False, null=False, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    book = models.ForeignKey(
        Book, blank=False, on_delete=models.CASCADE, null=False, related_name="ratings"
    )
    user = models.ForeignKey(
        User, blank=False, on_delete=models.CASCADE, null=False, related_name="ratings"
    )

    def __str__(self):
        return f"Rating: {self.rating} from Book: {self.book}, user: {self.user}, "


class Comment(models.Model):
    comment = models.CharField(blank=False, null=False, max_length=200)
    book = models.ForeignKey(
        Book, blank=False, on_delete=models.CASCADE, null=False, related_name="comment"
    )
    user = models.ForeignKey(
        User, blank=False, on_delete=models.CASCADE, null=False, related_name="comment"
    )
    comment_date_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment: {self.comment} from Book: {self.book}, user: {self.user}, date: {self.commentdate}"


class Favorite(models.Model):
    book = models.ForeignKey(
        Book,
        blank=False,
        on_delete=models.CASCADE,
        null=False,
        related_name="favorites",
    )
    user = models.ForeignKey(
        User,
        blank=False,
        on_delete=models.CASCADE,
        null=False,
        related_name="favorites",
    )

    def __str__(self):
        return f"Favorite Book: {self.book}, user: {self.user}"
