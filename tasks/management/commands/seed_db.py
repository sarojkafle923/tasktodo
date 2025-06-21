import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from tasks.models import Task, CustomUser  # Replace 'your_app' with your tasks app's name

class Command(BaseCommand):
    help = 'Seed database with test users and tasks dynamically'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=3,
            help='Number of users to create'
        )
        parser.add_argument(
            '--tasks-per-user',
            type=int,
            default=5,
            help='Number of tasks to create per user'
        )

    def handle(self, *args, **options):
        user_count = options['users']
        tasks_per_user = options['tasks_per_user']

        self.stdout.write(self.style.NOTICE(f'Seeding database with {user_count} users, each with {tasks_per_user} tasks...'))

        priorities = ['low', 'medium', 'high']
        statuses = ['pending', 'in_progress', 'completed', 'cancelled']

        users = []
        for i in range(user_count):
            email = f'user{i+1}@example.com'
            first_name = f'First{i+1}'
            last_name = f'Last{i+1}'
            password = 'password123'

            user, created = CustomUser.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'is_active': True,
                    'is_staff': False,
                }
            )
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created user: {email}'))
            else:
                self.stdout.write(self.style.WARNING(f'User already exists: {email}'))

            users.append(user)

        # Create tasks for each user
        for user in users:
            task_count = random.randint(max(1, tasks_per_user - 2), tasks_per_user + 2)  # +/- 2 variability
            for j in range(task_count):
                start_offset = random.randint(-5, 5)
                end_offset = start_offset + random.randint(1, 10)
                start_date = timezone.now() + timedelta(days=start_offset)
                end_date = timezone.now() + timedelta(days=end_offset)

                task = Task.objects.create(
                    title=f'Task {j+1} for {user.email}',
                    description=f'Description for task {j+1} assigned to {user.get_full_name()}',
                    user=user,
                    status=random.choice(statuses),
                    priority=random.choice(priorities),
                    start_date=start_date,
                    end_date=end_date
                )
                self.stdout.write(self.style.SUCCESS(f'Created task: {task.title}'))

        self.stdout.write(self.style.SUCCESS('Database seeding complete!'))
