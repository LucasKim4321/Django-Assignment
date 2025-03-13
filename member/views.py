from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, logout as django_logout
from django.urls import reverse
from django.contrib.auth.models import User

def sign_up(request):

    form = UserCreationForm(request.POST or None)
    if form.is_valid(): # 요구 조건 통과 여부 확인
        form.save() # 요구 조건이 맞으면 저장
        return redirect(settings.LOGIN_URL)

    context = {
        'form':form,
    }
    return render(request, 'registration/signup.html', context)

def login(request):
    form = AuthenticationForm(request, request.POST or None)

    if form.is_valid(): # 요구 조건 통과 여부 확인
        django_login(request, form.get_user())  # 로그인을 시도함
        return redirect(reverse('todo:list'))  # html의 {% url 'blog_list' %} 와 동일

    context = {
        'form':form
    }
    return render(request, 'registration/login.html', context)


def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users':users})

def user_info(request, user_id):
    user = User.objects.get(pk = user_id)
    return render(request, 'user_info.html', {'user':user} )
    # return render(request, 'user_info.html', {'user':users[user_id-1]} )