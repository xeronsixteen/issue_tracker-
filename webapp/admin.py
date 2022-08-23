from django.contrib import admin

# Register your models here.
from webapp.models import Task, Type, Status, TaskType, Project


class TaskAdmin(admin.ModelAdmin):
    list_display = ['project', 'id', 'summary', 'description', 'status', 'created_at']
    list_display_links = ['summary']
    list_filter = ['status']
    search_fields = ['summary', 'status']
    fields = ['summary', 'description', 'status']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['type']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'description']


admin.site.register(Task, TaskAdmin)
admin.site.register(Type)
admin.site.register(Status)
admin.site.register(TaskType)
admin.site.register(Project)
