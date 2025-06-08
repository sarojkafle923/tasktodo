from time import strftime
from django.http import HttpResponse
from django.shortcuts import render
from .models import Task

# Create your views here.
# def list_tasks(request):
#     data=Task.objects.all()
#     return HttpResponse(data)

def list_tasks(request):
    tasks = Task.objects.all()
    print(tasks)
    # Build a plain text response from tasks
    response_text = "Tasks List:\n"
    for task in tasks:
        response_text += f"- {task.name}: {task.description}\n"
        response_text += f"- {task.created.strftime("%d-%m-%Y %I:%M %p")}\n"
        response_text += f"- {'Task Completed' if task.isCompleted else 'Not Done'}"
        response_text += "\n_______________________________________________________\n"
    return HttpResponse(response_text, content_type='text/plain')
