from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from todo_list.models import Todo
from todo_list.forms import TodoForm
from django.urls import reverse

def todo_list(request):
    todo_list = Todo.objects.all().order_by('-created_at')

    q = request.GET.get('q')
    if q:
        todo_list = todo_list.filter(Q(title__icontains=q) | Q(description__icontains=q))

    paginator = Paginator(todo_list, 10)
    page = request.GET.get('page')
    page_object = paginator.get_page(page)

    # visit을 키값으로 쿠키를 가져오고 존재하지 않으면 0 있으면 +1
    visits = int(request.COOKIES.get('visits', 0 )) + 1

    request.session['count'] = request.session.get('count',0) + 1

    context = {
        # 'todo_list':todo_list,
        'count':request.session['count'],
        'page_obj':page_object,
        'object_list':page_object.object_list,
    }

    response = render(request, 'todo_list.html', context)
    response.set_cookie('visits', visits)

    return response

def todo_info(request, todo_id):
    todo = get_object_or_404(Todo, pk = todo_id)
    context = { 'todo': todo, }
    return render(request, 'todo_info.html', context)
@login_required
def todo_create(request):

    # 로그인되어 있지 않으면 로그인화면으로 리다이렉트
    # if not request.user.is_authenticated:
    #     return redirect(reverse('login'))

    # if request.method == 'POST':
    #     form = TodoForm(request.POST)
    #     if form.is_valid():
    #         todo = form.save() # form.save() : form에 내용을 DB에 반영하고 해당 데이터의 객체를 반환(리턴)함.
    #         return redirect(reverse('todo_info'), {'todo_id':todo.id})
    # else:
    #     form = TodoForm()

    form = TodoForm(request.POST or None)
    if form.is_valid():
        # form.save() : form에 내용을 DB에 반영하고 해당 데이터의 객체를 반환(리턴)함.
        todo = form.save(commit=False)  # DB에 반영하지 않고 객체만 반환함.
        todo.author = request.user  # 작성자에 로그인된 유저를 넣음
        todo.save()  # DB에 반영
        return redirect(reverse('fbv_todo:info', kwargs={'todo_id':todo.id}))

    context = {
        'form':form,
    }

    return render(request, 'todo_create.html', context)


@login_required
def todo_update(request, todo_id):
    # todo = get_object_or_404(Todo, pk=id)
    # if request.user != todo.author:
    #     raise Http404
    todo = get_object_or_404(Todo, pk=todo_id, author=request.user) # id author가 일치하는 데이터만 가져옴

    form = TodoForm(request.POST or None, instance=todo)  # instance 폼의 항목에 맞게 blog에서 데이터를 불러옴
    if form.is_valid():
        # form.save() : form에 내용을 DB에 반영하고 해당 데이터의 객체를 반환(리턴)함.
        todo = form.save()  # DB에 반영
        return redirect(reverse('fbv_todo:info', kwargs={'todo_id':todo.id}))

    context = {
        'todo':todo,
        'form':form,
   }

    return render(request, 'todo_form.html', context)


@login_required
@require_http_methods(['POST'])
def todo_delete(request, todo_id):
    # if request.method != 'POST':
    #     raise Http404

    todo = get_object_or_404(Todo, pk=todo_id, author=request.user) # pk와 author가 일치하는 데이터만 가져옴
    todo.delete()

    return redirect(reverse('fbv_todo:list'))



# 관리자 계정 생성
# python3 manage.py createsuperuser

# 데이터 추가
# todo_list = [Todo(title=f'할 일 {i}', description=f'할 일 설명 {i}', start_date='2025-01-11', end_date='2025-01-25') for i in range(1,11)]
# Todo.objects.bulk_create(todo_list)

# 서버 실행
# python3 manage.py runserver