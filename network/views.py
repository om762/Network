from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.urls import reverse
import json

from .models import User, Post, Comment


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

@login_required(login_url='/login')
def new_post(request):
    content = request.POST.get('content')
    if (content == ''):
        return HttpResponse('Bad Request, Empty Post Content' , status=400)
    Post.objects.create(poster=request.user, content=content).save()
    
    return HttpResponseRedirect('/')


def posts(request):
    page = int(request.GET.get('page') or 1)
    
    
    all_posts = Post.objects.all().order_by('-post_at')
    for p in all_posts:
        print(p.post_at)
    
    paginator = Paginator(all_posts, 10)
    try:
        posts = paginator.page(page)
    except:
        return JsonResponse({'message':'Invalid Page Number'}, status=400)
    
    post_data = []
    for post in posts:
        post_data.append({
            'id': post.id,
            'content': post.content,
            'poster': {
                'id': post.poster.id,
                'username': post.poster.username,
                'color': post.poster.color
            },
            'posting_date': post.post_at,
            'update_at': post.update_at,
            'likes': post.likes(),
            'is_liked': post.is_liked_by(request.user) if request.user.is_authenticated else False,
            'comments': post.comment_count()
        })
        
    page_data = {
        "current_page": page,
        "total_pages": paginator.num_pages,
        "has_next": posts.has_next(),
        "has_previous": posts.has_previous(),
    }
    return JsonResponse({
        'page_data':page_data,
        'posts':post_data
        }, safe=False)

login_required(login_url='/login')
def like_post(request):
    post_id = request.GET.get('post_id')
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return HttpResponse('Bad Request, Post id don\'t exist' , status=400)
    
    post.toggle_like(request.user)
    
    return JsonResponse({
        'likes': post.likes(),
        'is_liked': post.is_liked_by(request.user)
        }) 

def view_comments(request, post_id):
    if not Post.objects.filter(id=post_id).exists():
        return HttpResponse(f"There is such Post with id: {post_id}")
    
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(comment_on=post).order_by('-commented_at')
    return render(request, "network/comments.html", {
        "comments": comments,
        "post": post
    })

@login_required(login_url='/login')
@csrf_exempt
def comment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = int(data.get("post_id"))
        post = Post.objects.get(id=post_id)
        comment_text = data.get("commentText")
        Comment.objects.create(comment_on=post, commenter=request.user, comment=comment_text).save()
        return HttpResponseRedirect(f"/comments/{post_id}")