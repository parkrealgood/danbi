from django.contrib import admin

from task.models import Task, SubTask


class SubTaskInline(admin.TabularInline):
    model = SubTask
    fields = ['team', 'is_complete', 'completed_date']
    extra = 0


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'create_user', 'team', 'title', 'is_complete', 'completed_date']
    search_fields = ['title']
    list_filter = ['team', 'is_complete']
    raw_id_fields = ['create_user', 'team']
    inlines = [SubTaskInline]


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'task', 'team', 'is_complete', 'completed_date']
    list_filter = ['team', 'is_complete']
    raw_id_fields = ['task', 'team']
