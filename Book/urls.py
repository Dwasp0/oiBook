from django.urls import path

from . import views

app_name = "Book"

urlpatterns =  [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.loginview, name="login"),
    path("logout/", views.logoutview, name="logout"),
    path("pages/<int:page_id>/", views.detail, name="detail"),
    path("pages/<int:page_id>/exercises/", views.exercise, name="exercise"),
    path("search/", views.search, name="search"),
]
