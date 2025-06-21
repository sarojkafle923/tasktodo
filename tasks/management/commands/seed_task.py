import random
from datetime import timedelta
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.utils import timezone

from tasks.models import Task  # Replace with your actual app name


class Command(BaseCommand):
    help = "Seed Task model with test data"

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email of the user to assign tasks to')
        parser.add_argument('--today', type=int, default=0, help='Number of tasks for today')
        parser.add_argument('--tomorrow', type=int, default=0, help='Number of tasks for tomorrow')
        parser.add_argument('--upcoming', type=int, default=0, help='Number of tasks for upcoming days (day +2 and later)')
        parser.add_argument('--overdue', type=int, default=0, help='Number of overdue tasks')

    def handle(self, *args, **options):
        email = options['email']
        custom_user = get_user_model()

        try:
            user = custom_user.objects.get(email=email)
        except custom_user.DoesNotExist:
            raise CommandError(f"User with email '{email}' does not exist.")

        self.stdout.write(self.style.SUCCESS(f"Seeding tasks for user: {email}"))

        status_choices = [choice[0] for choice in Task.STATUS_CHOICES]
        priority_choices = [choice[0] for choice in Task.PRIORITY_CHOICES]

        def create_tasks(count, start_offset, end_offset):
            for _ in range(count):
                start_date = timezone.now() + timedelta(days=start_offset)
                end_date = timezone.now() + timedelta(days=end_offset)

                Task.objects.create(
                    user=user,
                    title=f"Task {random.randint(1000, 9999)}",
                    description="This is a seeded task.",
                    status=random.choice(status_choices),
                    priority=random.choice(priority_choices),
                    start_date=start_date,
                    end_date=end_date
                )

        create_tasks(options['today'], 0, 1)
        create_tasks(options['tomorrow'], 1, 2)
        create_tasks(options['upcoming'], 2, 5)
        create_tasks(options['overdue'], -5, -1)

        self.stdout.write(self.style.SUCCESS("✅ Task seeding completed."))
