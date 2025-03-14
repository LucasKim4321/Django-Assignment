from django import forms
from todo_list.models import Todo, Comment

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        # fields = '__all__'  # 전체 적용
        fields = ('title', 'description', 'start_date', 'end_date', 'is_completed')  # 원하는 것만 적용

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        # 특정 필드에 TextInput 삽입
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control'})  # content필드에 textinput 삽입
        }
        # Comment 모델이 가지고있는 verbose_name 쓰지 않고 따로 지정
        labels = {
            'content': '댓글'
        }