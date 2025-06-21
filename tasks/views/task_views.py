from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.template import TemplateDoesNotExist, TemplateSyntaxError
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from typing import Dict, List, Any, Optional

from tasks.forms import TaskForm
from tasks.models import Task
from tasks.constants import RouteGroup


class TaskSectionConfig:
    """Configuration class for task sections"""

    def __init__(self, key: str, queryset_func, page_param: str, empty_message: str):
        self.key = key
        self.queryset_func = queryset_func
        self.page_param = page_param
        self.empty_message = empty_message


class TaskListView(LoginRequiredMixin, ListView):
    """Enhanced task list view with better separation of concerns"""

    model = Task
    template_name = RouteGroup.PROTECTED.TASKS.LIST.template_path
    context_object_name = 'task_sections'
    paginate_by = 5

    def get_queryset(self):
        """Get base queryset filtered by current user"""
        return Task.objects.filter(
            user=self.request.user
        ).select_related('user').order_by('-start_date')

    @staticmethod
    def get_section_configs(base_queryset, today: timezone.now().date) -> List[TaskSectionConfig]:
        """Define section configurations"""
        tomorrow = today + timedelta(days=1)
        day_after_tomorrow = today + timedelta(days=2)

        return [
            TaskSectionConfig(
                key='today',
                queryset_func=lambda: base_queryset.filter(start_date__date=today),
                page_param='today_page',
                empty_message='No tasks scheduled for today.'
            ),
            TaskSectionConfig(
                key='tomorrow',
                queryset_func=lambda: base_queryset.filter(start_date__date=tomorrow),
                page_param='tomorrow_page',
                empty_message='No tasks scheduled for tomorrow.'
            ),
            TaskSectionConfig(
                key='upcoming',
                queryset_func=lambda: base_queryset.filter(start_date__date__gte=day_after_tomorrow),
                page_param='upcoming_page',
                empty_message='No upcoming tasks scheduled.'
            ),
        ]

    def paginate_section(self, config: TaskSectionConfig) -> Dict[str, Any]:
        """Paginate a specific section"""
        from django.core.paginator import Paginator

        page_number = self.request.GET.get(config.page_param, 1)
        queryset = config.queryset_func()
        paginator = Paginator(queryset, self.paginate_by)
        page_obj = paginator.get_page(page_number)

        return {
            'key': config.key,
            'page_obj': page_obj,
            'empty_message': config.empty_message,
        }

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """Enhanced context data with proper structure"""
        context = super().get_context_data(**kwargs)

        base_queryset = self.get_queryset()
        today = timezone.now().date()
        now = timezone.now()

        section_configs = self.get_section_configs(base_queryset, today)
        task_sections = [self.paginate_section(config) for config in section_configs]

        context.update({
            'task_sections': task_sections,
            'now': now,
        })

        return context

    def get_section_context(self, section_key: str) -> Optional[Dict[str, Any]]:
        """Get context for a specific section (for AJAX requests)"""
        base_queryset = self.get_queryset()
        today = timezone.now().date()
        now = timezone.now()

        section_configs = self.get_section_configs(base_queryset, today)

        # Find the requested section
        config = next((c for c in section_configs if c.key == section_key), None)
        if not config:
            return None

        section_data = self.paginate_section(config)

        return {
            'task_list': section_data['page_obj'],
            'section': section_data['key'],
            'page_obj': section_data['page_obj'],
            'empty_message': section_data['empty_message'],
            'now': now,
        }

    def get(self, request, *args, **kwargs):
        """Handle both regular and AJAX requests"""
        # Handle AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return self.handle_ajax_request(request)

        # Handle regular requests
        return super().get(request, *args, **kwargs)

    def handle_ajax_request(self, request) -> JsonResponse:
        """Handle AJAX pagination requests"""
        section = request.GET.get('section')

        if not section:
            return JsonResponse({'error': 'Section parameter required'}, status=400)

        section_context = self.get_section_context(section)

        if not section_context:
            return JsonResponse({'error': 'Invalid section'}, status=400)

        try:
            html = render_to_string(
                'protected/tasks/partials/task_list_content.html',
                section_context,
                request
            )
            return JsonResponse({'html': html})
        except (TemplateDoesNotExist, TemplateSyntaxError) as e:
            return JsonResponse({'error': f'Template rendering failed: {str(e)}'}, status=500)


class TaskCreateView(LoginRequiredMixin, CreateView):
    """View for creating new tasks"""

    model = Task
    form_class = TaskForm
    template_name = 'protected/tasks/task_form.html'
    success_url = reverse_lazy(RouteGroup.PROTECTED.TASK_ADD.url_name)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)