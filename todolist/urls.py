from django.urls import path
from todolist.views import show_todolist, create_task, register_user, login_user, logout_user

app_name = 'todolist'

urlpatterns = [
    path('', show_todolist, name='show_todolist'),
    path('create-task/', create_task, name='create_task'),
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user')
]