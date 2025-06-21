from django import template
from django.utils import timezone

register = template.Library()

def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    if total_seconds < 0:
        total_seconds = abs(total_seconds)
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    if days > 0:
        return f"{days} day{'s' if days != 1 else ''}"
    elif hours > 0:
        return f"{hours} hour{'s' if hours != 1 else ''}"
    elif minutes > 0:
        return f"{minutes} minute{'s' if minutes != 1 else ''}"
    else:
        return f"{seconds} second{'s' if seconds != 1 else ''}"

@register.filter
def humanize_timedelta(value, now=None):
    if not value:
        return ""
    if not now:
        now = timezone.now()
    diff = value - now
    return format_timedelta(diff)
