from django.shortcuts import render, get_object_or_404
from todo_list.models import Todo

def todo_list(request):
    todo_list = Todo.objects.all()

    # visit을 키값으로 쿠키를 가져오고 존재하지 않으면 0 있으면 +1
    visits = int(request.COOKIES.get('visits', 0 )) + 1

    request.session['count'] = request.session.get('count',0) + 1

    context = {
        'todo_list':todo_list,
        'count':request.session['count'],
    }

    response = render(request, 'todo_list.html', context)
    response.set_cookie('visits', visits)

    return response

def todo_info(request, todo_id):
    todo_info = get_object_or_404(Todo, id = todo_id)
    context = { 'todo_info': todo_info, }
    return render(request, 'todo_info.html', context)

# 관리자 계정 생성
# python3 manage.py createsuperuser

# 데이터 추가
# todo_list = [Todo(title=f'할 일 {i}', description=f'할 일 설명 {i}', start_date='2025-01-11', end_date='2025-01-25') for i in range(1,11)]
# Todo.objects.bulk_create(todo_list)

# 서버 실행
# python3 manage.py runserver