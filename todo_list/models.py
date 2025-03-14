from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from utils.models import TimestampModel

User = get_user_model()

class Todo(TimestampModel):
    title = models.CharField('제목', max_length=50)
    description = models.TextField(verbose_name='설명')
    start_date = models.DateField(verbose_name='시작일')  # "2025-01-25" 이런식으로 입력
    end_date = models.DateField(verbose_name='마감일')  # "2025-01-25" 이런식으로 입력
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # author_id
    # models.CASCATE => 같이 삭제 => 유저 삭제시 같이 블로그도 같이 삭제
    # models.PROTECT => 삭제가 불가능함 => 유저를 삭제하려고 할 때 블로그가 있으면 유저 삭제가 불가능 (기본값)
    # models.SET_NULL => 널 값을 넣음 => 유저 삭제시 블로그의 author가 Null이 됨.

    # 기존에 없던 author를 외례키로 추가하면 기존 블로그의 author값이 없어서 마이그레이션 할 때 에러남
    # python3 manage.py makemigrations 하면 기존 블로그 데이터에 기본값을 줄건지 물어봄.
    # 1번 기본값 주기 선택 후 기존 데이터의 초기값으로 주어질 id값 선택 하면 정상적으로 마이그레이션 됨.
    is_completed = models.BooleanField('완료', default=False)

    # TimestampModel에서 created_at, updated_at을 상속받음
    # created_at = models.DateTimeField('생성일', auto_now_add=True)
    # modified_at = models.DateTimeField('수정일', auto_now=True)

    # 관리자 페이지에서 bookmark object 라고 표시되는 사항 변경
    def __str__(self):
        return self.title

    # get_absolute_url은 보통 detail페이지
    def get_absolute_url(self):
        return reverse('todo:info', kwargs={'pk':self.pk})

    class Meta:
        verbose_name = '할 일'
        verbose_name_plural = '할 일 리스트'
        # pass


class Comment(TimestampModel):
    # TimestampModel에서 created_at, updated_at을 상속받음
    # created_at = models.DateTimeField('작성일자', auto_now_add=True)
    # updated_at = models.DateTimeField('수정일자', auto_now_add=True)
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    content = models.CharField('본문', max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __stf__(self):
        return f'{self.todo.title} 댓글'

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'
        ordering = ('-created_at', '-id',) # 댓글 최신순으로 정렬
