from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.logind, name="login"),
    path("logout", views.logoutd, name="logout"),
    path("RightNow", views.rightNow, name="rightNow"),
    path("Saw", views.Saw, name="Saw"),
    path("Species", views.species, name="Species"),
    path("me/<str:user>", views.me, name="me"),
]
