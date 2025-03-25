from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path, include, reverse
from django.views import View
from django.views.generic import TemplateView

from todo.views import todo_list, todo_info, todo_create, todo_update, todo_delete
from users import views as user_views

def index(request):
    # return redirect('/todo/')
    return redirect(reverse('cbv_todo_list'))
# def user_list(request):
#     return render(request, 'user_list.html', {'users':users})
# def user_info(request, user_id):
#     return render(request, 'user_info.html', {'user':next((user for user in users if user['id'] == user_id), None)} )
#     # return render(request, 'user_info.html', {'user':users[user_id-1]} )
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name = 'index'),
    path('todo/', todo_list, name='todo_list'),
    path('todo/create/', todo_create, name='todo_create'),
    path('todo/<int:todo_id>/', todo_info, name='todo_info'),
    path('todo/<int:todo_id>/update/', todo_update, name='todo_update'),
    path('todo/<int:todo_id>/delete/', todo_delete, name='todo_delete'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', user_views.login, name='login'),
    path('accounts/signup/', user_views.sign_up, name='signup'),
    # CBV URL include
    path('cbv/', include('todo.urls')),
    # summernote URL include
    path('summernote/', include('django_summernote.urls')),
]


# config.settings 보단 django.conf의 settings가 나음.
# 현재 장고 실행환경에서 셋팅을 불러옴.  배포환경에서는 경로가 달라질 수 있기 때문에 이렇게함.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
