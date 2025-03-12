from django import forms
from todo_list.models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        # fields = '__all__'  # 전체 적용
        fields = ('title', 'description', 'start_date', 'end_date', 'is_completed')  # 원하는 것만 적용