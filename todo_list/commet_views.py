from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from todo_list.forms import CommentForm
from todo_list.models import Todo, Comment

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    # fields = ["content"]
    form_class = CommentForm

    # post요청만 받기 위해 get 요청시 에러 발생
    def get(self, *args, **kwargs):
        raise Http404

    def form_valid(self, form):
        todo = self.get_todo()
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.todo = todo
        self.object.save()
        return HttpResponseRedirect(reverse('todo:info', kwargs={'todo_pk':todo.pk} ))

    def get_todo(self):
        pk = self.kwargs['todo_pk']
        todo = get_object_or_404(Todo, pk=pk)
        return todo

# /comment/create/<int:todo_pk>/

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'comment_pk'  # url에서 pk말고 다른 이름으로 id값 가져올 시 설정

    # post요청만 받기 위해 get 요청시 에러 발생
    def get(self, *args, **kwargs):
        raise Http404("GET 요청은 허용되지 않습니다.")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.author != self.request.user:
            raise Http404("수정 권한이 없습니다.")
        return self.object

    # update 성공 시 동작
    # get_success_url이 없으면 model의 get_absolute_url찾아서 처리
    def get_success_url(self):
        return reverse_lazy('todo:info', kwargs={'todo_pk': self.object.todo.pk})

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    pk_url_kwarg = 'comment_pk'  # url에서 pk말고 다른 이름으로 id값 가져올 시 설정

    def get(self, *args, **kwargs):
        raise Http404  # GET 요청 차단

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not (self.request.user == obj.author or self.request.user.is_superuser):
            raise Http404("삭제 권한이 없습니다.")
        return obj

    def get_success_url(self):
        # URL에서 받은 todo_pk를 그대로 사용
        return reverse_lazy('todo:info', kwargs={'todo_pk': self.object.todo.pk})