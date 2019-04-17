from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model, update_session_auth_hash
from .forms import CustomUserChangeForm, ProfileForm, CustomUserCreationForm
from .models import Profile


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
            
            # GET으로 들어온 값중 'next'가 가진 값을 가져온다
            # next가 저의되어 있으면 해당 url로 redirect
            # else: post:list로 redirect
            return redirect(request.GET.get('next') or 'posts:list')
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
    
    
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            auth_login(request, user)
            return redirect('posts:list')
    else:
        form = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'form': form})
        
        
def people(request, username):
    # information about user
    people = get_object_or_404(get_user_model(), username=username)
    return render(request, 'accounts/people.html', { 'people': people })
    

# change account information(editting & updating)
# @login_required
def update(request):
    if request.method == "POST":
        # updating
        user_change_form = CustomUserChangeForm(data=request.POST, instance=request.user)
        profile_form = ProfileForm(data=request.POST, instance=request.user.profile)
        
        if user_change_form.is_valid() and profile_form.is_valid():
            user = user_change_form.save()
            profile_form.save()
            return redirect('people', user.username)
        
    else:
        # editting
        user_change_form = CustomUserChangeForm(instance=request.user)
        
        # 1. instance에 넣어줄 profile이 있는 user와 없는 user가 있다
        profile, created = Profile.objects.get_or_create(user=request.user)
        
        profile_form = ProfileForm(instance=profile)
        
        context = {
            'user_change_form': user_change_form,
            'profile_form': profile_form,
        }
        
        return render(request, 'accounts/update.html', context)
        
        
def delete(request):
    if request.method == "POST":
        request.user.delete()
        return redirect('accounts:signup')
    
    return render(request, 'accounts/delete.html')
    

def password(request):
    if request.method == "POST":
        password_change_form = PasswordChangeForm(request.user, request.POST)
        
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
        
            return redirect('people', request.user.username)
    else:
        password_change_form = PasswordChangeForm(request.user)
        context = {
            'password_change_form': password_change_form
        }
        
        return render(request, 'accounts/password.html', context)
    
    
def follow(request, user_id):
    follower = get_object_or_404(get_user_model(), pk=user_id)
    
    # 만약 현재 유저가 해당 유저를 이미 팔로우 하고 있다면
    # 팔로우 취소
    if request.user != follower:
        if request.user in follower.followers.all() :
            follower.followers.remove(request.user)
        else:
            follower.followers.add(request.user)
    
    return redirect('people', follower.username)