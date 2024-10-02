from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login,logout


def home(request):
    return render(request , 'chat/index.html')



def index(request):
    return render(request, "chat/index1.html")

def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')  # 'login' is the name of your login URL
    else:
        form = UserRegisterForm()
    return render(request, 'chat/register.html', {'form': form})




def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome {username}! You are logged in.')
                return redirect('index')  # 'home' is the name of your homepage URL
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'chat/login.html', {'form': form})




def logout_user(request):
    logout(request)
    return redirect('login') 
