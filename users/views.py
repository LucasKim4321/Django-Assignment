from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as django_login


def sign_up(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid(): # 요구 조건 통과 여부 확인
        form.save() # 요구 조건이 맞으면 저장
        return redirect(settings.LOGIN_URL)

    context = {'form': form}
    return render(request, 'registration/signup.html', context)


def login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid(): # 요구 조건 통과 여부 확인
        django_login(request, form.get_user())  # 로그인을 시도함
        return redirect(settings.LOGIN_REDIRECT_URL)  # LOGIN_REDIRECT_URL로 리다이렉트

    context = {'form': form}
    return render(request, 'registration/login.html', context)
