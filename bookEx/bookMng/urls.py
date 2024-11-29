from django.urls import path

from bookMng import views

urlpatterns = [
    path("", views.displaybook, name="index"),
    path("displaybooks", views.displaybook, name="displaybooks"),
    path("postbook", views.postbook, name="postbook"),
    path("mybooks", views.mybooks, name="mybooks"),
    path("book_detail/<int:book_id>", views.book_detail, name="book_detail"),
    path("deletebook/<int:book_id>", views.deletebook, name="deletebook"),
    path("aboutus", views.aboutus, name="aboutus"),

    path("api/getFavoriteBooks", views.getFavoriteBooks, name="getFavoriteBooks"),
    path("api/toggleFavoritesByBookID/<int:book_id>", views.toggleFavoritesByBookID, name="toggleFavoritesByBookID"),
]
