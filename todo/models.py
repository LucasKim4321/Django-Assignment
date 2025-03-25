from django.contrib.auth import get_user_model
from django.db import models
from PIL import Image
from pathlib import Path
from io import BytesIO

from django.urls import reverse

from utils.models import TimestampModel

User = get_user_model()


class Todo(TimestampModel):
    # TimestampModel에서 created_at, updated_at을 상속받음
    # created_at = models.DateTimeField('작성일자', auto_now_add=True)
    # updated_at = models.DateTimeField('수정일자', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(verbose_name='설명')
    start_date = models.DateField(verbose_name='시작일')  # "2025-01-25" 이런식으로 입력
    end_date = models.DateField(verbose_name='마감일')  # "2025-01-25" 이런식으로 입력
    # models.CASCATE => 같이 삭제 => 유저 삭제시 같이 블로그도 같이 삭제
    # models.PROTECT => 삭제가 불가능함 => 유저를 삭제하려고 할 때 블로그가 있으면 유저 삭제가 불가능 (기본값)
    # models.SET_NULL => 널 값을 넣음 => 유저 삭제시 블로그의 author가 Null이 됨.

    # 기존에 없던 author를 외례키로 추가하면 기존 블로그의 author값이 없어서 마이그레이션 할 때 에러남
    # python3 manage.py makemigrations 하면 기존 블로그 데이터에 기본값을 줄건지 물어봄.
    # 1번 기본값 주기 선택 후 기존 데이터의 초기값으로 주어질 id값 선택 하면 정상적으로 마이그레이션 됨.
    is_completed = models.BooleanField('완료', default=False)
    thumbnail = models.ImageField(upload_to='todo/thumbnails', default='todo/no_image/NO-IMAGE.gif', null=True, blank=True)
    completed_image = models.ImageField(upload_to='todo/completed_images', null=True, blank=True)

    # TimestampModel에서 created_at, updated_at을 상속받음
    # created_at = models.DateTimeField('생성일', auto_now_add=True)
    # modified_at = models.DateTimeField('수정일', auto_now=True)

    # 관리자 페이지에서 bookmark object 라고 표시되는 사항 변경
    def __str__(self):
        return self.title

    # get_absolute_url은 보통 detail페이지
    def get_absolute_url(self):
        return reverse('todo:info', kwargs={'todo_pk':self.pk})

    class Meta:
        verbose_name = '할 일'
        verbose_name_plural = '할 일 리스트'

    def save(self, *args, **kwargs):
        if not self.completed_image:
            return super().save(*args, **kwargs)

        image = Image.open(self.completed_image)
        image.thumbnail((100, 100))

        image_path = Path(self.completed_image.name)

        thumbnail_name = image_path.stem
        thumbnail_extension = image_path.suffix
        thumbnail_filename = f'{thumbnail_name}_thumbnail{thumbnail_extension}'

        if thumbnail_extension in ['.jpg', '.jpeg']:
            file_type = 'JPEG'
        elif thumbnail_extension == '.png':
            file_type = 'PNG'
        elif thumbnail_extension == '.gif':
            file_type = 'GIF'
        else:
            return super().save(*args, **kwargs)

        temp_thumb = BytesIO()
        image.save(temp_thumb, format=file_type)
        temp_thumb.seek(0)

        self.thumbnail.save(thumbnail_filename, temp_thumb, save=False)

        temp_thumb.close()
        return super().save(*args, **kwargs)


class Comment(TimestampModel):
    # TimestampModel에서 created_at, updated_at을 상속받음
    # created_at = models.DateTimeField('작성일자', auto_now_add=True)
    # updated_at = models.DateTimeField('수정일자', auto_now_add=True)
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=200)

    def __str__(self):
        return f'{self.user}: {self.message}'

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'
        ordering = ('-created_at', '-id',) # 댓글 최신순으로 정렬


# models.py 변경 휴 마이그레이션
# python manage.py makemigrations # 마이그레이션 파일 생성
# python manage.py migrate # 마이그레이션 적용