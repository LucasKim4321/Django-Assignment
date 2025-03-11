from django.contrib import admin
from todo_list.models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'start_date','end_date','is_completed']
    list_display_links = ['title','description']
    list_filter = ['title','start_date','end_date','is_completed']
