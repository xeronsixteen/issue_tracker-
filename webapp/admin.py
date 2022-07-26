from django.contrib import admin

# Register your models here.
from webapp.models import Task, Type, Status, TaskType, Project


class TaskAdmin(admin.ModelAdmin):
    list_display = ['project name', 'id', 'summary', 'description', 'status', 'created_at', 'type']
    list_display_links = ['summary']
    list_filter = ['status', 'project name']
    search_fields = ['summary', 'status', 'project name']
    fields = ['summary', 'description', 'status', 'type']
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Task)
admin.site.register(Type)
admin.site.register(Status)
admin.site.register(TaskType)
admin.site.register(Project)