from django.contrib import admin

# Register your models here.
from webapp.models import Task, Type, Status


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'status', 'created_at', 'updated_at', 'type', 'summary']
    list_display_links = ['summary']
    list_filter = ['status']
    search_fields = ['description', 'status']
    fields = ['summary', 'description', 'status', 'type']
    # readonly_fields = ['Date']


admin.site.register(Task, TaskAdmin)
admin.site.register(Type)
admin.site.register(Status)
