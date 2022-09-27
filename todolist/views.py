import datetime
from todolist.models import Task
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
@login_required(login_url='/todolist/login/')
def show_todolist(request):
    task_list = Task.objects.all() 

    context = {
        "task_list": task_list,
        "username": request.user.get_username()
    }
    
    return render(request, "todolist.html", context)

def register_user(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('todolist:login_user')

    context = {
        'form': form
    }

    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            response =  HttpResponseRedirect(reverse('todolist:show_todolist'))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

        else:
            messages.info(request, 'Username atau Password anda salah!')
    
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('todolist:login_user'))
    response.delete_cookie('last_login')
    return response