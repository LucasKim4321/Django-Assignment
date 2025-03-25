from django.db import models

class TimestampModel(models.Model):
    created_at = models.DateTimeField('작성일자', auto_now_add=True)
    updated_at = models.DateTimeField('수정일자', auto_now=True)

    class Meta:
        abstract = True

# Meta 클래스에서 abstract = True를 설정하면, 이 모델이 데이터베이스 테이블로 생성되지 않고
# 다른 모델이 이를 상속받아 사용할 수 있도록 하는 "추상 모델(Abstract Model)"이 됩니다.
