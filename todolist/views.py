import datetime
from todolist.models import Task
from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

class CreateTaskForm(forms.Form):
    title = forms.CharField(label="Judul Task")
    description = forms.CharField(label="Deskripsi Task")

# Create your views here.
@login_required(login_url='/todolist/login/')
def show_todolist(request):
    task_list = Task.objects.filter(user = request.user).all()

    context = {
        "task_list": task_list,
        "username": request.user.get_username()
    }
    
    return render(request, "todolist.html", context)

@login_required(login_url='/todolist/login/')
def create_task(request):
    if request.method == "POST":
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            new_task = Task(
                date = datetime.datetime.now(),
                title = form.cleaned_data["title"],
                description = form.cleaned_data["description"],
                user = request.user
            )
            new_task.save()
            return redirect("todolist:show_todolist")

        messages.warning(request, "Pembuatan task gagal!")
    
    form = CreateTaskForm()
    context = {"form": form}
    return render(request, "createtask.html", context=context)

@login_required(login_url='/todolist/login/')
def modify_task(request):
    if request.method == "POST":
        pk = request.POST.get("task_pk")
        task = Task.objects.get(pk = pk)
        action = request.POST.get("action")
        
        # Validasi requesting user == pemilik task untuk menghindari modifikasi oleh user lain
        if request.user == task.user:
            if action == "finish":
                task.is_finished = True
            elif action == "unfinish":
                task.is_finished = False
            task.save()
    return HttpResponseRedirect(reverse('todolist:show_todolist'))

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