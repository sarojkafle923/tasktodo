from time import strftime
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Task

# Create your views here.

# ------ Authentication Views ------
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

class LoginView(CreateView):
    template_name = 'login.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

# ------ Task Views ------
def list_task(request):
    tasks = Task.objects.all()
    
    # Build a plain text response from tasks
    response_text = "Tasks List:\n"
    for task in tasks:
        response_text += f"- {task.title}: {task.description}\n"
        response_text += f"- {task.created_at.strftime("%d-%m-%Y %I:%M %p")}\n"
        response_text += f"- {'Task Completed' if task.completed else 'Not Done'}"
        response_text += "\n_______________________________________________________\n"
    return HttpResponse(response_text, content_type='text/plain')
