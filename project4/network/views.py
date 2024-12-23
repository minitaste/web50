from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Post


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def new_post(request):
    if request.method == 'POST':
        author = request.user
        text = request.POST["text"]

        if not text.strip():
            return render(request, "network/new_post.html", {
                "error": "Text can`t be blank.",
            })
        
        new_post = Post.objects.create(author=author, text=text)

        return redirect("index")

    return render(request, "network/new_post.html")


def all_posts(request):
    return render(request, "network/all_posts.html", {
        "posts": Post.objects.all(),
    })


def profile(request, username):
    try:
        user = User.objects.get(username=username)
        posts = Post.objects.filter(author=user)
        
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("index")
    
    return render(request, "network/profile.html", {
        "user": user,
        "posts": posts,
    })