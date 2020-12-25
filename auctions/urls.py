from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("creatListing", views.createListings, name="createListings"),
    path("listings/<int:listing>", views.listing, name="listing")
]
