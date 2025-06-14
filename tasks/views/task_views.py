from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from tasks.constants import RouteGroup
from tasks.models import Task

class ListTaskView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        """Render the tasks page"""
        tasks = Task.objects.filter(user_id=request.user.id)
        print(tasks)
        return render(request, RouteGroup.PROTECTED.TASKS.LIST.template_path)
