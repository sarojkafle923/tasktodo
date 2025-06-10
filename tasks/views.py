from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib import messages
from tasks.forms import CustomUserCreationForm
from .models import Task

# Create your views here.

# ------ Authentication Views ------
class RegisterView(FormView):
    template_name = "register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("tasks")
    
    def form_valid(self, form):
        # this method is called when the form data has been POSTed.
        form.save()  # Save the new user to the database
        messages.success(self.request, "Registration successful! You can now log in.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Handle invalid form submissions"""
        messages.error(self.request, "There were errors in your form. Please correct them and try again.")
        # For normal form submission
        return super().form_invalid(form)
    
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
