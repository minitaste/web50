from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, Page
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
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
        "posts": Post.objects.all().order_by('-created_at'),
    })


def profile(request, username):
    try:
        user = User.objects.get(username=username)
        posts = Post.objects.filter(author=user).order_by('-created_at')
        is_following = False

        if request.user.is_authenticated:
            is_following = user.followers.filter(id=request.user.id).exists()

    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("index")
    
    return render(request, "network/profile.html", {
        "user_profile": user,
        "posts": posts,
        "is_following": is_following,
    })


@login_required
def toggle_follow(request, username):
    if request.method == "POST":
        user_to_follow = get_object_or_404(User, username=username)
        if user_to_follow == request.user:
            return JsonResponse({"error": "You cannot follow yourself."}, status=400)

        if request.user in user_to_follow.followers.all():
            user_to_follow.followers.remove(request.user)
            is_following = False
        else:
            user_to_follow.followers.add(request.user)
            is_following = True

        return JsonResponse({
            "is_following": is_following,
            "followers_count": user_to_follow.followers.count()
        })

    return JsonResponse({"error": "Invalid request method."}, status=400)


@login_required
def following(request):
    user = request.user 
    following = user.followings.all()

    posts = Post.objects.filter(author__in=following).order_by('-created_at')
    
    paginator = Paginator(posts, 10)

    
    
    return render(request, "network/following.html", {
        "posts": posts,
    })