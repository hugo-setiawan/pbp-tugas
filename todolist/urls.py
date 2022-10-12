from django.urls import path
from todolist.views import *

app_name = 'todolist'

urlpatterns = [
    path('', show_todolist, name='show_todolist'),
    path('json/', get_todolist_json, name='get_todolist_json'),
    path('create-task/', create_task, name='create_task'),
    path('add/', create_task_ajax, name='create_task_ajax'),
    path('modify-task/', modify_task, name='modify_task'),
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user')
]