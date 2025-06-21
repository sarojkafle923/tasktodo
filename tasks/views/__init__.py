from .auth_views import RegisterView
from .task_views import TaskListView, TaskCreateView
from .core_views import HomeView

# This file imports the views from the tasks app and makes them available for use.
__all__ = [
    'RegisterView',
    'TaskListView',
    'TaskCreateView',
    'HomeView']