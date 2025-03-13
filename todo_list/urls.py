from django.urls import path
from todo_list import views as todo_views

app_name = 'fbv_todo'

urlpatterns = [
    path('', todo_views.todo_list, name='list'),
    path('<int:todo_id>/', todo_views.todo_info, name='info'),
    path('create/', todo_views.todo_create, name='create'),
    path('<int:todo_id>/update/', todo_views.todo_update, name='update'),
    path('<int:todo_id>/delete/', todo_views.todo_delete, name='delete'),
]