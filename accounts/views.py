from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.
def login(request):
    if request.method == "POST":
        #로그인 검증
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        
        # login_user = authenticate(request, username=username, password=password)
        
        # 더 쉬운 방법
        form = AuthenticationForm(request, request.POST)
        
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('posts:list')
        #로그인 시킨다
        # if login_user is not None:
        #     auth_login(request, login_user)
        #     return redirect('posts:list')
    else:
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    
    return redirect('posts:list')
        