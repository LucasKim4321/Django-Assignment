from django.urls import path
from todo_list import cb_views as todo_views

app_name = 'todo'

urlpatterns = [
    path('', todo_views.TodoListView.as_view(), name='list'),
    path('<int:pk>/', todo_views.TodoDetailView.as_view(), name='info'),
    path('create/', todo_views.TodoCreateView.as_view(), name='create'),
    path('<int:pk>/update/', todo_views.TodoUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', todo_views.TodoDeleteView.as_view(), name='delete'),
]