from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from todo_list.forms import CommentForm
from todo_list.models import Todo, Comment


class TodoListView(ListView):
    # model = Todo # object.all()을 사용해 데이터를 가져옴.
    # ordering = ('-created_at',)  # 정렬 옵션
    queryset = Todo.objects.all().order_by('-created_at')  # 사용자 지정 query
    template_name = 'todo_list.html'  # render()할 페이지
    paginate_by = 10  # paginator 설정

    # 사용자 지정 쿼리셋
    def get_queryset(self):
        queryset = super().get_queryset()  # 쿼리 셋을 가져옴
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(content__icontains = q)
            )
        return queryset

# context = {
#     "paginator": paginator,
#     "page_obj": page,
#     "is_paginated": is_paginated,
#     "object_list": queryset,
# }

# 기존 디테일 뷰
# class TodoDetailView(DetailView):
#     model = Todo
#     template_name = 'todo_info.html'

# 상세 페이지에서 댓글 페이지 기능을 사용하기 위해 리스트뷰를 사용
class TodoDetailView(ListView):  # 댓글
    model = Comment
    template_name = 'todo_info.html'
    paginate_by = 10

    # pk_url_kwarg = 'todo_id'  # url에서 pk말고 다른 이름으로 id값 가져올 시 설정

    # 블로그 정보 불러옴.
    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Todo, pk=kwargs.get('todo_pk'))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(todo=self.object).prefetch_related('author')
    # pk_url_kwarg = 'todo_id'  # url에서 pk말고 다른 이름으로 id값 가져올 시 설정

    # 데이터 처리하는 방법 1
    # 사용자 지정 쿼리셋
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(id__lte=50)

    # 데이터 처리하는 방법 2
    # def get_object(self, queryset=None):
    #     # object = self.model.objects.get(pk=self.kwargs.get('pk'))
    #     object = super().get_object()
    #     if object.id > 50:
    #         raise Http404("해당 객체에 대한 접근이 금지되어있습니다.")
    #     return object

    # 사용자 지정 context
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['test'] = 'CBV'
    #     return context

# LoginRequiredMixin  @login_required 와 동일한 기능
class TodoCreateView(LoginRequiredMixin,CreateView):
    model = Todo
    template_name = 'todo_create.html'
    # form 설정
    # fields = '__all__'  # 전체 적용
    fields = ('title', 'description', 'start_date', 'end_date', 'is_completed')  # 원하는 것만 적용
    # success_url = reverse('cb_todo_list') # 서로가 서로를 임포트하는 서큘러 임포트가 발생
    # success_url = reverse_lazy('cb_todo_list')  # create 성공시 동작
    # success_url = reverse_lazy('cb_todo_info', kwargs={'pk':object.pk})  # 오류남.

    # 작성자 생성 후 save()동작
    def form_valid(self, form):
        # todo = form.save(commit=False)
        # todo.object = form.save(commit=False)
        # todo.object.author = self.request.user
        # todo.object.save()
        # self.object = todo
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    # create 성공 시 동작
    def get_success_url(self):
        return reverse_lazy('todo:info', kwargs={'pk':self.object.pk})

class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    template_name = 'todo_update.html'
    fields = ('title', 'description', 'start_date', 'end_date', 'is_completed')  # 원하는 것만 적용

    # 로그인 유저와 작성자가 같을 때만 수정 가능하게 처리
    # 1
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(author=self.request.user)
    # 2
    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #     if self.object.author != self.request.user:
    #         raise Http404
    #     return self.object

    # update 성공 시 동작
    # def get_success_url(self):
        # return reverse_lazy('cb_todo_info', kwargs={'pk':self.object.pk})
    # get_success_url이 없으면 model의 get_absolute_url찾아서 처리

class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo

    # 로그인 유저와 작성자가 같을 때만 삭제 가능하게 처리
    def get_queryset(self):
        queryset = super().get_queryset()
        # superuser가 아니면 로그인 유저와 글쓴이가 동일한 데이터만 반환
        # 조건문이 많아지면 not으로 쓰는걸 더 추천한다고 함.
        if not self.request.user.is_superuser:
            return queryset.filter(author=self.request.user)
        return queryset

    # delete 성공 시 동작
    def get_success_url(self):
        return reverse_lazy('todo:list')


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def get(self, *args, **kwargs):
        raise Http404

    def form_valid(self, form):
        todo = self.get_todo()
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.todo = todo
        self.object.save()
        return HttpResponseRedirect(reverse('todo:detail', kwargs={'todo_pk':todo.pk} ))

    def get_todo(self):
        pk = self.kwargs['todo_pk']
        todo = get_object_or_404(Todo, pk=pk)
        return todo

# /comment/create/<int:todo_pk>/
