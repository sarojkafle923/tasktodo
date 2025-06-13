from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from tasks.constants import RouteGroup

class HomeView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        """Render the index page"""
        return render(request, RouteGroup.PROTECTED.HOME.template_path)
  