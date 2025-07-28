from django import forms

from tasks.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'start_date', 'end_date', 'status', 'priority']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'title': forms.TextInput(attrs={'placeholder': 'Enter task title'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Task Title',
            'description': 'Task Description',
            'start_date': 'Start Date and Time',
            'end_date': 'End Date and Time',
            'status': 'Status',
            'priority': 'Priority Level',
        }