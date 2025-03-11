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
from django.urls import path
from django.shortcuts import render, redirect
from fake_db import users

def index(request):
    return redirect('/users/')
def user_list(request):
    return render(request, 'user_list.html', {'users':users})
def user_info(request, user_id):
    return render(request, 'user_info.html', {'user':next((user for user in users if user['id'] == user_id), None)} )
    # return render(request, 'user_info.html', {'user':users[user_id-1]} )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('users/', user_list),
    path('users/<int:user_id>/', user_info),
]
