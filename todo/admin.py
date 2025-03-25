from django.contrib import admin
from todo.models import Todo, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ('message', 'user')


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'description', 'is_completed', 'start_date', 'end_date')  # 관리자 목록 페이지에 보여줄 컬럼
    list_filter = ('is_completed',)  # 필터 사이드바에 표시할 필드
    search_fields = ('title',)  # 검색창을 통해 검색할 수 있는 필드
    ordering = ('start_date',)  # 생성일 기준으로 최신순 정렬
    list_display_links = ('title',)  # 목록에서 content를 클릭하면 상세 페이지로 이동
    fieldsets = (  # 댓글 수정 페이지에서 필드를 그룹으로 나눠 보여 줌
        ('Todo Info', {
            'fields': ('user', 'title', 'description', 'completed_image', 'is_completed')
        }),
        ('Date Range', {
            'fields': ('start_date', 'end_date')
        }),
    )
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'todo', 'user', 'message', 'created_at')
    list_filter = ('todo', 'user')
    search_fields = ('message', 'user')
    ordering = ('-created_at',)
    list_display_links = ('message',)
    fieldsets = (
        ('Comment Info', {
            'fields': ('todo', 'user', 'message')
        }),
    )
