from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .forms import PostForm
from .models import *
from .utils import paginatePosts
import json
from django.contrib import messages



def index(request):
    posts = Post.objects.all().order_by("-created").all()
    posts, custom_paginator = paginatePosts(request, posts, 10)
    if request.user.is_authenticated:
        user_likes = [like.post.id for like in request.user.user_likes.all()]
    else:
        user_likes = []
    return render(request, "network/index.html", {
        "post_form": PostForm(),
        "posts": posts,
        "posts_type": "All Posts",
        'custom_paginator': custom_paginator,
        'user_likes': user_likes,
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
            return redirect(request.GET['next'] if request.GET.get('next') else 'index')
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return redirect(request.GET['next'] if request.GET.get('next') else 'index')


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if (not username) or (not email) or (not password):
            return render(request, "network/register.html", {
                "message": "You must fill out all fields."
            })

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
        return redirect(request.GET['next'] if request.GET.get('next') else 'index')
    else:
        return render(request, "network/register.html")


def add_post(request):
    owner = request.user
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = owner
            post.save()
            return redirect(request.GET['next'] if request.GET.get('next') else 'index')


def edit_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.user == post.user:
        content = json.loads(request.body)['content']
        post.content = content
        post.save()
        return JsonResponse({
            'content': content
        })
    messages.error(request, 'You can\'t edit others posts')
    return JsonResponse({
            'e': 'You can\'t edit others posts'
        })


def delete_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.user == post.user:
        print('here')
        post.delete()
        return JsonResponse({
            'result': 'Post deleted successfully'
        })
    messages.error(request, 'You can\'t delete others posts')
    return JsonResponse({
        'e': 'You Can\'t delete others posts'
    })


def comment(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == "POST":
        content = json.loads(request.body)['content']
        owner = request.user
        comment = Comment(post=post, content=content, user=owner)
        comment.save()
        return JsonResponse({
            'content': f'{comment.content}',
            'user': f'{owner}',
            'user_id': f'{owner.id}',
            'username': f'{owner.username}',
        })


def like(request, post_id):
    if request.method == "POST":
        try:
            like = Like.objects.get(
                user=request.user, post=Post.objects.get(pk=post_id))
        except Like.DoesNotExist:
            new_like = Like(user=request.user,
                            post=Post.objects.get(pk=post_id))
            new_like.save()
            result = 'Like added'
        else:
            like.delete()
            result = 'Like removed'
    post_likes = Post.objects.get(id=post_id).post_likes.all().count()
    return JsonResponse({
        'likes_count': post_likes,
        'result': result
    })


def profile(request, user_pk):
    user_profile = User.objects.get(pk=user_pk)
    posts = user_profile.user_posts.order_by("-created").all()
    posts, custom_paginator = paginatePosts(request, posts, 10)
    if request.user.is_authenticated:
        user_likes = [like.post.id for like in request.user.user_likes.all()]
    else:
        user_likes = []
    following = user_profile.following.all()
    followers = user_profile.followers.all()
    is_following = False
    for i in followers:
        if request.user.id == i.user_following.id:
            is_following = True
            print('here')

    return render(request, "network/profilepage.html", {
        "user_profile": user_profile,
        "user_posts": posts,
        'edit_form': PostForm(),
        'custom_paginator': custom_paginator,
        'following': following,
        'followers': followers,
        'is_following': is_following,
        'user_likes': user_likes,

    })


def follow_unfollow(request, user_pk):
    if request.method == "POST":
        try:
            follow = Follow.objects.get(
                user_following=request.user.id, user_followed=user_pk)
        except Follow.DoesNotExist:
            try:
                user_to_follow = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponse(status=404)
            else:
                new_follow = Follow(user_following=request.user,
                                    user_followed=user_to_follow)
                new_follow.save()
        else:
            follow.delete()

        return redirect(request.GET['next'] if request.GET.get('next') else 'index')


def following(request):
    current_user = User.objects.get(pk=request.user.pk)
    users_posts = [follow_obj.get_user_followed_posts()
                   for follow_obj in current_user.following.all()]
    posts = [post for user in users_posts for post in user]
    posts, custom_paginator = paginatePosts(request, posts, 10)
    if request.user.is_authenticated:
        user_likes = [like.post.id for like in request.user.user_likes.all()]
    else:
        user_likes = []
    return render(request, "network/index.html", {
        "post_form": PostForm(),
        "posts": posts,
        "posts_type": "Following Posts",
        'custom_paginator': custom_paginator,
        'user_likes': user_likes,

    })
