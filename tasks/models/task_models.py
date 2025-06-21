from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

class TaskQuerySet(models.QuerySet):
    """Custom QuerySet for Task model with additional methods if needed."""
    def for_user(self, user):
        """Filter tasks for a specific user."""
        return self.filter(user=user)

    def today(self):
        today = timezone.now().date()
        return self.filter(start_date__date=today)

    def tomorrow(self):
        tomorrow = timezone.now().date() + timedelta(days=1)
        return self.filter(start_date__date=tomorrow)

    def upcoming(self):
        day_after_tomorrow = timezone.now().date() + timedelta(days=2)
        return self.filter(start_date__date__gte=day_after_tomorrow)

    def overdue(self):
        now = timezone.now()
        return self.filter(end_date__lt=now, status__in=['pending', 'in_progress'])

    def by_priority(self):
        priority_order = models.Case(
            models.When(priority='high', then=models.Value(1)),
            models.When(priority='medium', then=models.Value(2)),
            models.When(priority='low', then=models.Value(3)),
            default=models.Value(4),
            output_field=models.IntegerField(),
        )
        return self.annotate(priority_order=priority_order).order_by('priority_order', '-start_date')

class TaskManager(models.Manager):
    """Custom manager for Task model with additional methods if needed."""
    def get_queryset(self) -> TaskQuerySet:
        return TaskQuerySet(self.model, using=self._db)

    def for_user(self, user):
        return self.get_queryset().for_user(user)

    def today(self):
        return self.get_queryset().today()

    def tomorrow(self):
        return self.get_queryset().tomorrow()

    def upcoming(self):
        return self.get_queryset().upcoming()

    def overdue(self):
        return self.get_queryset().overdue()

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    # Basic fields
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)

    # User relationship
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks', db_index=True)

    # Status and priority
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', db_index=True)

    # Dates
    start_date = models.DateTimeField(default=timezone.now, db_index=True)
    end_date = models.DateTimeField(db_index=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Custom manager
    objects = TaskManager()

    class Meta:
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['user', 'start_date']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['start_date', 'end_date']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tasks:detail', kwargs={'pk': self.pk})

    @property
    def is_overdue(self):
        """Check if the task is overdue."""
        return (
                self.end_date < timezone.now() and
                self.status in ['pending', 'in_progress']
        )

    @property
    def days_until_due(self):
        """Get days until due date"""
        delta = self.end_date.date() - timezone.now().date()
        return delta.days

    def clean(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError('End date must be before start date')

    def save(self, *args, **kwargs):
        """Override save method to ensure end date is after start date."""
        self.full_clean()
        super().save(*args, **kwargs)
