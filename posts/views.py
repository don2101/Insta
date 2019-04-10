from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post
from django.views.decorators.http import require_POST

# Create your views here.


def create(request):
    if request.method == "POST":
        # store written post in DB
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts:list')
    else:
        # return form to write form
        form = PostForm()
        return render(request, 'posts/create.html', {'form': form})


def list(request):
    # show all post
    posts = Post.objects.all()
    
    return render(request, 'posts/list.html', {'posts': posts})


def delete(request, post_num):
    post = Post.objects.get(id=post_num)
    post.delete()
    
    return redirect('posts:list')
    

def update(request, post_num):
    if request.method == 'GET':
        post = Post.objects.get(id=post_num)
        form = PostForm(instance=post)
        
        context = {}
        context['form'] = form
        context['post'] = post
        
        return render(request, 'posts/update.html', context=context)
    else:
        post = Post.objects.get(id=post_num)
        post.content = request.POST.get('content')
        post.save()
        return redirect('posts:list')
