from django.shortcuts import render, redirect
from .forms import PostForm

# Create your views here.


def create(request):
    if request.method == "POST":
        # store written post in DB
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts:create')
    else:
        # return form to write form
        form = PostForm()
        return render(request, 'posts/create.html', {'form': form})
