from django.contrib import admin
from tasks.models import Task

# Register your models here.

# Define the admin interface for the Task model.
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'start_date', 'end_date', 'created_at')
    list_filter = ('status', 'user')
    search_fields = ('title', 'description')

admin.site.register(Task, TaskAdmin)