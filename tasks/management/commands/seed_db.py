from django.core.management import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from tasks.models import CustomUser, Task

EMAIL_TEMPLATE = "user{}@test.com"
DEFAULT_PASSWORD = "password"

class Command(BaseCommand):
    help = "Seed the database with users and tasks for testing purposes."

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=5, help='Number of users to create.')
        parser.add_argument('--tasks', type=int, default=10, help='Number of tasks per user to create.')

    def handle(self, *args, **options):
        num_users = options['users']
        tasks_per_user = options['tasks']

        for i in range(num_users):
            email = EMAIL_TEMPLATE.format(i)
            user, created = CustomUser.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': f'FirstName{i}',
                    'last_name': f'LastName{i}',
                    'is_active': True,
                }
            )

            if created:
                user.set_password(DEFAULT_PASSWORD)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created user: {email}'))
            else:
                self.stdout.write(self.style.WARNING(f'User already exists: {email}'))

            # Create tasks for the user
            now = timezone.now()
            for j in range(tasks_per_user):
                if j < 5:
                    start = now - timedelta(days=random.randint(10, 30))
                    end = start + timedelta(hours=random.randint(1, 5))
                elif j < 10:
                    start = now - timedelta(hours=random.randint(0, 12))
                    end = now + timedelta(hours=random.randint(1, 12))
                else:
                    start = now + timedelta(days=random.randint(1, 30))
                    end = start + timedelta(hours=random.randint(1, 5))

                Task.objects.create(
                    user=user,
                    title=f"Task {j+ 1} for {email}",
                    description=f"Auto-generated task #{j+ 1}",
                    completed=random.choice([True, False]),
                    start_date=start,
                    end_date=end
                )
                self.stdout.write(self.style.SUCCESS(f'Created task for user {email}: Task {j + 1}'))
        self.stdout.write(self.style.SUCCESS('Done'))