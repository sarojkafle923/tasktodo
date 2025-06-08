from time import strftime
from django.http import HttpResponse
from django.shortcuts import render
from .models import Task

def list_task(request):
    tasks = Task.objects.all()
    
    # Build a plain text response from tasks
    response_text = "Tasks List:\n"
    for task in tasks:
        response_text += f"- {task.name}: {task.description}\n"
        response_text += f"- {task.created.strftime("%d-%m-%Y %I:%M %p")}\n"
        response_text += f"- {'Task Completed' if task.isCompleted else 'Not Done'}"
        response_text += "\n_______________________________________________________\n"
    return HttpResponse(response_text, content_type='text/plain')
