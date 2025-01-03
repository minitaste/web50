
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-post", views.new_post, name="new-post"),
    path("all-posts", views.all_posts, name="all-posts"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("follow/<str:username>", views.toggle_follow, name="toggle-follow"),
    path("following/", views.following, name="following"),
]

