from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

def index(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        
        #call the name of the tag element, name is the reference key
        content = request.POST["content"]
        Post.objects.create(content=content, user=request.user)
        return HttpResponseRedirect(reverse("index"))
    else:
        all_post = Post.objects.all().order_by("-created_at")
        paginator = Paginator(all_post, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html", {
            "page_obj": page_obj
        })


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

def profile(request, username):
    user = User.objects.get(username=username)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        if "unfollow" in request.POST:
            Followers.objects.get(user=user, follower=request.user).delete()
        elif "follow" in request.POST:
            Followers.objects.create(user=user, follower=request.user)
        else:
            print("Error: wrong input name")
        return HttpResponseRedirect(reverse("profile", args=(username)))    

    user_follow = False
    if request.user.is_authenticated:
        user_follow = request.user.following.filter(user=user.id).exists()

    # use the posts in the model Post.user as the key to reference the content
    user_post = user.posts.order_by("-created_at").all()
    paginator = Paginator(user_post, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
        "user": user,
        "user_post": user_post,
        "page_obj": page_obj,
        "following_profile": user_follow
    })

@login_required
def following(request):
    user = User.objects.get(id=request.user.id)
    followed_user = [follow.user for follow in user.following.all()]
    # __in to get all the items in the list
    posts = Post.objects.filter(user__in = followed_user).order_by("-created_at")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "followed_user": followed_user
    })

@csrf_exempt
def postedit(request):
    if request.method != "PUT":
        return JsonResponse({"error": "Request must be PUT, to edit."}, status=400)

    data = json.loads(request.body)
    post_id = data.get("post_id", "")
    post = Post.objects.get(id=post_id)

    content = data.get("content")
    liked = data.get("liked")
    if content:
        if request.user != post.user:
            return JsonResponse({'error': "Not the owner of the post."})
        post.content = content
    if liked:
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
    post.save()
    return JsonResponse({'message': 'Successful edit', 'likes': str(post.likes.count())}, status=200)