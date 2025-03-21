from django.urls import path
from todo_list import cb_views as todo_views, commet_views

app_name = 'todo'

urlpatterns = [
    path('', todo_views.TodoListView.as_view(), name='list'),
    path('<int:todo_pk>/', todo_views.TodoDetailView.as_view(), name='info'),
    path('create/', todo_views.TodoCreateView.as_view(), name='create'),
    path('<int:todo_pk>/update/', todo_views.TodoUpdateView.as_view(), name='update'),
    path('<int:todo_pk>/delete/', todo_views.TodoDeleteView.as_view(), name='delete'),
    path('comment/create/<int:todo_pk>/', commet_views.CommentCreateView.as_view(), name = 'comment-create'),
    path('comment/update/<int:comment_pk>/', commet_views.CommentUpdateView.as_view(), name = 'comment-update'),
    path('comment/delete/<int:comment_pk>/', commet_views.CommentDeleteView.as_view(), name = 'comment-delete'),
]