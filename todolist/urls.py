from django.urls import path
from todolist.views import register_user, login_user

app_name = 'todolist'

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
]