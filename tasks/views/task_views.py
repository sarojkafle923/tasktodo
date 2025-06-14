from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from tasks.constants import RouteGroup
from tasks.models import Task

class ListTaskView(LoginRequiredMixin, View):
    tasks = Task.objects.all()

    # Build a plain text response from tasks
    response_text = "Tasks List:\n"
    for task in tasks:
        response_text += f"- {task.title}: {task.description}\n"
        response_text += f"- {task.created_at.strftime("%d-%m-%Y %I:%M %p")}\n"
        response_text += f"- {'Task Completed' if task.completed else 'Not Done'}"
        response_text += "\n_______________________________________________________\n"

    @staticmethod
    def get(request):
        """Render the tasks page"""
        return render(request, RouteGroup.PROTECTED.TASKS.LIST.template_path)
