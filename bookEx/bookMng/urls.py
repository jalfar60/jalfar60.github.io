from django.urls import path

from bookMng import views

urlpatterns = [
    path("", views.displaybook, name="index"),
    path("postbook", views.postbook, name="postbook"),
    path("displaybooks", views.displaybook, name="displaybooks"),
    path("user/<int:user_id>", views.displayUser, name="displayUser"),
    path("mybooks", views.mybooks, name="mybooks"),
    path("favoriteBooks", views.favoriteBooks, name="favoriteBooks"),
    path("book_detail/<int:book_id>", views.book_detail, name="book_detail"),
    path("deletebook/<int:book_id>", views.deletebook, name="deletebook"),
    path("aboutus", views.aboutus, name="aboutus"),

    path("api/getFavoriteBooks", views.getFavoriteBooks, name="getFavoriteBooks"),
    path("api/toggleFavoritesByBookID/<int:book_id>", views.toggleFavoritesByBookID, name="toggleFavoritesByBookID"),
]
