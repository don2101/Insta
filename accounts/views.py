from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate


# Create your views here.
def login(request):
    if request.method == "POST":
        #로그인 검증
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        login_user = authenticate(request, username=username, password=password)
        #로그인 시킨다
        if login_user is not None:
            auth_login(request, login_user)
            return redirect('posts:list')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.user:
        auth_logout(request)
    
    return redirect('posts:list')
        