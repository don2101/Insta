from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post
from django.views.decorators.http import require_POST

# Create your views here.


def create(request):
    if request.method == "POST":
        # store written post in DB
        form = PostForm(request.POST, request.FILES)
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
