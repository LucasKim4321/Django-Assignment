"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect
from fake_db import users
from todo_list import views as todo_views
from member import views as member_views

def index(request):
    return redirect('/todo/')
def user_list(request):
    return render(request, 'user_list.html', {'users':users})
def user_info(request, user_id):
    return render(request, 'user_info.html', {'user':next((user for user in users if user['id'] == user_id), None)} )
    # return render(request, 'user_info.html', {'user':users[user_id-1]} )
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name = 'index'),
    path('users/', user_list, name = 'user_list'),
    path('users/<int:user_id>/', user_info, name = 'user_info'),
    path('todo/', todo_views.todo_list, name = 'todo_list'),
    path('todo/<int:todo_id>/', todo_views.todo_info, name = 'todo_info'),
    path('todo/create/', todo_views.todo_create, name = 'todo_create'),
    path('todo/<int:todo_id>/update/', todo_views.todo_update, name = 'todo_update'),
    path('todo/<int:todo_id>/delete/', todo_views.todo_delete, name = 'todo_delete'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', member_views.sign_up, name = 'signup'),
    path('login/', member_views.login, name = 'login')
]
