from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q

from todo.forms import CommentForm, TodoForm, TodoUpdateForm
from todo.models import Todo, Comment

from django.core.paginator import Paginator


class TodoListView(LoginRequiredMixin, ListView):
    # model = Todo # object.all()을 사용해 데이터를 가져옴.
    queryset = Todo.objects.all()  # 사용자 지정 queryset
    template_name = 'todo/todo_list.html'  # render()할 페이지
    paginate_by = 10  # paginator 설정
    ordering = ['-created_at']  # 정렬 옵션

    # get_queryset override
    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)  # 쿼리 셋을 가져옴
        if self.request.user.is_superuser:
            queryset = super().get_queryset()

        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(content__icontains=q))
        return queryset

    # context = {
    #     "paginator": paginator,
    #     "page_obj": page,
    #     "is_paginated": is_paginated,
    #     "object_list": queryset,
    # }
    #
    # # 기존 디테일 뷰
    # class TodoDetailView(DetailView):
    #     model = Todo
    #     template_name = 'todo_info.html'

class TodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    queryset = Todo.objects.all().prefetch_related('comments', 'comments__user')
    template_name = 'todo/todo_info.html'
    # pk_url_kwarg = 'todo_pk'  # url에서 pk말고 다른 이름으로 id값 가져올 시 설정

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("해당 To Do를 조회할 권한이 없습니다.")
        return obj

    def get_context_data(self, **kwargs):
        comments = self.object.comments.order_by('-created_at')
        paginator = Paginator(comments, 5)
        context = {
            'todo': self.object.__dict__,
            'comment_form': CommentForm(),
            'page_obj':  paginator.get_page(self.request.GET.get('page'))
        }
        return context


# LoginRequiredMixin  @login_required 와 동일한 기능
class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    template_name = 'todo/todo_create.html'
    # 기존에 fields를 선언하여 form을 생성하던 방법에서 TodoForm을 불러와서 사용
    form_class = TodoForm
    # fields = ('title', 'description', 'start_date', 'end_date', 'is_completed')  # 원하는 것만 적용
    # success_url = reverse('cb_todo_list') # 서로가 서로를 임포트하는 서큘러 임포트가 발생
    # success_url = reverse_lazy('cb_todo_list')  # create 성공시 동작
    # success_url = reverse_lazy('cb_todo_info', kwargs={'pk':object.pk})  # 오류남

    # 작성자 생성 후 save()동작
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    # create 성공 시 동작
    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.id})


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    template_name = 'todo/todo_update.html'
    # 기존에 fields를 선언하여 form을 생성하던 방법에서 TodoForm을 불러와서 사용
    form_class = TodoUpdateForm

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("해당 To Do를 수정할 권한이 없습니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.id})

    # update 성공 시 동작
    # def get_success_url(self):
        # return reverse_lazy('cb_todo_info', kwargs={'pk':self.object.pk})
    # get_success_url이 없으면 model의 get_absolute_url찾아서 처리

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_title'] = '수정'
        context['btn_name'] = '수정'
        return context

class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("해당 To Do를 삭제할 권한이 없습니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo_list')


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['message']
    pk_url_kwarg = 'todo_id'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.todo = Todo.objects.get(id=self.kwargs['todo_id'])
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.kwargs['todo_id']})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['message']

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("해당 댓글을 수정할 권한이 없습니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.todo.id})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("해당 댓글을 삭제할 권한이 없습니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.todo.id})