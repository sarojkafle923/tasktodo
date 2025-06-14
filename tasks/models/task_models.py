from django.db import models
from django.conf import settings

class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    start_date = models.DateTimeField(null=False, blank=False)
    end_date = models.DateTimeField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['completed', '-start_date', '-end_date', '-created_at']

    def clean(self):
        super().clean()
        if self.end_date and self.start_date and self.start_date >= self.end_date:
            from django.core.exceptions import ValidationError
            raise ValidationError({'end_date': 'End date must be after start date.'})
