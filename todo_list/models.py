from django.db import models

class Todo(models.Model):
    title = models.CharField('제목', max_length=50)
    description = models.TextField(verbose_name='설명')
    start_date = models.DateField(verbose_name='시작일')  # "2025-01-25" 이런식으로 입력
    end_date = models.DateField(verbose_name='마감일')  # "2025-01-25" 이런식으로 입력
    is_completed = models.BooleanField('완료', default=False)
    created_at = models.DateTimeField('생성일', auto_now_add=True)
    modified_at = models.DateTimeField('수정일', auto_now=True)

    # 관리자 페이지에서 bookmark object 라고 표시되는 사항 변경
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '할 일'
        verbose_name_plural = '할 일 리스트'
        # pass