from django.contrib import admin
from todo_list.models import Todo, Comment

admin.site.register(Comment)

# TabularInline 표로 만들어서 inline으로 넣어주는 기능
class CommentInline(admin.TabularInline):
    model = Comment
    fields = ['content', 'author']
    extra = 1  # 기본 3개

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'start_date','end_date','is_completed']
    list_display_links = ['title','description'] # Admin 목록 페이지에서 보여줄 열(column)
    list_filter = ['title','start_date','end_date','is_completed'] # Admin 목록 우측에 필터.
    inlines = [
        CommentInline,
    ]

