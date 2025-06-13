from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib import messages

from tasks.constants import RouteGroup
from tasks.forms import CustomUserCreationForm
from tasktodo import settings

class RegisterView(FormView):
    """
    View for user registration.
    This view handles the registration form, validates the input,
    and creates a new user if the form is valid.
    """
    template_name = RouteGroup.AUTH.REGISTER.template_path
    form_class = CustomUserCreationForm
    success_url = reverse_lazy(settings.LOGIN_URL)  
    
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
