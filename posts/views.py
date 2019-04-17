from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm
from .models import Post, Comment
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def create(request):
    if request.method == "POST":
        # store written post in DB
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:list')
    else:
        # return form to write form
        form = PostForm()
        return render(request, 'posts/create.html', {'form': form})


def get_follower_posts(followers, posts):
    for follower in followers:
        posts.union(posts, follower.post_set.all())


def list(request):
    # show all post
    posts = request.user.post_set.all()
    comment_form = CommentForm()
    followers = request.user.followers.all()
    
    get_follower_posts(followers, posts)
    
    print(posts)
    
    context = {}
    context['posts'] = posts
    context['comment_form'] = comment_form
    context['followers'] = followers
    
    
    return render(request, 'posts/list.html', context=context)


@require_POST
def delete(request, post_num):
    post = get_object_or_404(Post, pk=post_num)
    
    if post.user != request.user:
        return redirect('posts:list')
    
    post.delete()
    
    return redirect('posts:list')
    

def update(request, post_num):
    post = get_object_or_404(Post, pk=post_num)
    
    if post.user != request.user:
        return redirect('posts:list')
    
    if request.method == 'GET':
        form = PostForm(instance=post)
        
        context = {}
        context['form'] = form
        
        return render(request, 'posts/update.html', context=context)
    else:
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:list')
            

@login_required
def like(request, post_num):
    # 1. get Post to like
    post = get_object_or_404(Post, pk=post_num)
    
    # 2. the user already liked this post, 
    #       remove like
    #    else
    #       add like
    
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    else:
        post.like_users.add(request.user)
    
    return redirect('posts:list')

@require_POST
@login_required
def create_comment(request, post_num):
    post = get_object_or_404(Post, id=post_num)
    
    form = CommentForm(request.POST)
    
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.post = post
        instance.save()
    
    return redirect('posts:list')


@require_POST    
@login_required
def delete_comment(request, post_num, comment_num):
    comment = get_object_or_404(Comment, id=comment_num)
    
    if request.user == comment.user:
        comment.delete()
        
    return redirect('posts:list')
    
    