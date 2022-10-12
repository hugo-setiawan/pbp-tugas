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
from django.utils.encoding import iri_to_uri
from django.utils.http import url_has_allowed_host_and_scheme
from django.core import serializers

# Form yang akan digunakan untuk membuat task baru
class CreateTaskForm(forms.Form):
    title = forms.CharField(label="Judul Task")
    description = forms.CharField(label="Deskripsi Task")

# View yang menunjukkan todolist kepada user
@login_required(login_url='/todolist/login/')
def show_todolist(request):
    task_list = Task.objects.filter(user = request.user).all()

    context = {
        "task_list": task_list,
        "username": request.user.get_username()
    }
    
    return render(request, "todolist.html", context)

def get_todolist_json(request):
    todolist = Task.objects.all()
    return HttpResponse(serializers.serialize("json", todolist), content_type="application/json")

# View untuk membuat task baru
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

        messages.warning(request, "Pembuatan task gagal! Periksa kembali input anda!")
    
    form = CreateTaskForm()
    context = {
        "form": form,
        "username": request.user.get_username()
    }
    return render(request, "createtask.html", context=context)

# View (endpoint) untuk memodifikasi task tertentu
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
                task.save()
            elif action == "unfinish":
                task.is_finished = False
                task.save()
            elif action == "toggle":
                task.is_finished = False if task.is_finished else True
                task.save()
            elif action == "delete":
                task.delete()

    return HttpResponse(serializers.serialize("json", [task]))

# View untuk meregistrasi user baru
def register_user(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('todolist:login_user')
        else:
            messages.error(request, 'Akun gagal dibuat! Periksa kembali input anda.')

    context = {
        'form': form
    }

    return render(request, 'register.html', context)

# View untuk login
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # redirect implementation https://stackoverflow.com/a/44807947
            next_url = request.GET.get('next')

            # redirect URL validation https://stackoverflow.com/a/60372947
            if next_url and url_has_allowed_host_and_scheme(next_url, None):
                next_url = iri_to_uri(next_url)
                response = HttpResponseRedirect(next_url)
            else:
                # default is normal todolist page
                response = HttpResponseRedirect(reverse('todolist:show_todolist'))

            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

        else:
            messages.error(request, 'Username atau Password anda salah!')
    
    context = {}
    return render(request, 'login.html', context)

# View untuk logout
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('todolist:login_user'))
    response.delete_cookie('last_login')
    return response