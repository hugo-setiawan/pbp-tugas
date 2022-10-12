from django.urls import path
from todolist.views import show_todolist, create_task, modify_task, register_user, login_user, logout_user, get_todolist_json

app_name = 'todolist'

urlpatterns = [
    path('', show_todolist, name='show_todolist'),
    path('json/', get_todolist_json, name='get_todolist_json'),
    path('create-task/', create_task, name='create_task'),
    path('modify-task/', modify_task, name='modify_task'),
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user')
]