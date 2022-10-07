from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from .models import User, Post, Profile
from .forms import EditProfile
import json
import random


def index(request):
    # Composing a new post
    if request.method == "POST":
        if request.user.is_authenticated:
            content = request.POST["content"]

            # Create Post for user
            Post.objects.create(author=request.user, content=content)
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("index"))
    else:
        allPosts = Post.objects.all()
        paginator = Paginator(allPosts, 10) # Show 10 posts per page

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html", {
            'page_obj': page_obj,
            'recommend_follow': recommend_follow(request),
            })
        
        
def recommend_follow(request):
    # Utility function to recommend followers to the user
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        user_followings = [profile.user for profile in user.followings.all()]
        non_followings = User.objects.exclude(username__in=user_followings).exclude(username=user)
        
        # Sample a list of profiles the user follows/not follows 
        if len(non_followings) >= 1:
            return {'title': 'You might like to follow',
                    'suggestions':random.sample(list(non_followings), 3 if len(non_followings) > 3 else len(non_followings))}
        else:
            return {'title': 'Some People you follow',
                    'suggestions':random.sample(list(user_followings), 3 if len(user_followings) > 3 else len(user_followings))}


@csrf_exempt
def profile(request, username):

    # Get the profile of the user
    profile_owner = User.objects.get(username=username)

    # Add/Remove a follower to/from a user profile
    if request.method == "PUT" and request.user.is_authenticated:
        data = json.loads(request.body)
        if data.get('user_wants_to_follow_profile_owner') == True:
            Profile.objects.create(user=profile_owner, follower=request.user)
            message = 'User follows profile'
        else:
            Profile.objects.get(user=profile_owner, follower=request.user).delete()
            message = 'User unfollows profile'
        return JsonResponse({"message": message}, status=201)

    # By default, a user doesn't follow any profile
    user_follows_profile_owner = False
    if request.user.is_authenticated:
        profile_owner_follows_user = request.user.followings.filter(user=profile_owner.id).exists()
        user_follows_profile_owner = profile_owner_follows_user
        
    # Get all posts made by the profile user
    profile_owner_posts = profile_owner.posts.all()
    paginator = Paginator(profile_owner_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
        'profile_owner_posts' : profile_owner_posts,
        'page_obj':page_obj,
        'profile_owner':profile_owner,
        'user_follows_profile_owner' : user_follows_profile_owner,
        'recommend_follow': recommend_follow(request),
    })

@csrf_exempt
@login_required
def editPost(request):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required"}, status=400)

    # Get edited content of user's post
    data = json.loads(request.body)
    edited_content = data.get('content')
    post_id = data.get('post_id')
    post = Post.objects.get(id=post_id) # get the post from the database for updating

    # Check that the users can only edit their posts
    if request.user != post.author:
        return JsonResponse({"error": "User can only edit their posts"})
    post.content = edited_content # update content of the post
    post.save()
    return JsonResponse({"message": "Post edited successfully"}, status=201)


@csrf_exempt
@login_required
def like_post(request):
    if request.method != 'PUT':
        return JsonResponse({"error": "PUT request required"}, status=400)

    data = json.loads(request.body)
    post_id = data.get('post_id')

    post = Post.objects.get(id=post_id)
    if request.user in post.liked_by.all():
        post.liked_by.remove(request.user)
        message = 'Unlike successful'
    else:
        post.liked_by.add(request.user)
        message = 'Like successful'
    post.save()
    return JsonResponse({"message": message, "like_count":str(post.get_like_count())}, status=201)


def editProfile(request, username):
    # Prepopulate the details of the user on the form
    form = EditProfile(instance=request.user)
    
    if request.POST:
        form = EditProfile(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile', args=(request.user.username,)))
    
    return render(request, "network/editProfile.html", context={'form':form,
                                                                'recommend_follow': recommend_follow(request)})

def following(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    user_following = [profile.user for profile in request.user.followings.all()] # Get a list of all followings
    allFollowingPosts = Post.objects.filter(author__in=user_following).order_by("-created_date") # Get the posts made by profiles that the user follows

    # Create a list of all posts made by profiles the user follows
    # allFollowingPosts = []
    # for profile in request.user.followings.all():
    #     allFollowingPosts.extend(profile.user.posts.all())

    paginator = Paginator(allFollowingPosts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        'page_obj':page_obj,
        'recommend_follow': recommend_follow(request)
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
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
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
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
