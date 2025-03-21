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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, reverse
from django.shortcuts import render, redirect
from fake_db import users
from todo_list import views as todo_views
from member import views as member_views

def index(request):
    # return redirect('/todo/')
    return redirect(reverse('todo:list'))
# def user_list(request):
#     return render(request, 'user_list.html', {'users':users})
# def user_info(request, user_id):
#     return render(request, 'user_info.html', {'user':next((user for user in users if user['id'] == user_id), None)} )
#     # return render(request, 'user_info.html', {'user':users[user_id-1]} )
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name = 'index'),
    path('users/', member_views.user_list, name = 'user_list'),
    path('users/<int:user_id>/', member_views.user_info, name = 'user_info'),
    path('fb/', include('todo_list.urls')),
    path('todo/', include('todo_list.cb_urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', member_views.sign_up, name = 'signup'),
    path('login/', member_views.login, name = 'login')
]

# config.settings 보단 django.conf의 settings가 나음.
# 현재 장고 실행환경에서 셋팅을 불러옴.  배포환경에서는 경로가 달라질 수 있기 때문에 이렇게함.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # django.conf.urls.static
