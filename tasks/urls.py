from django.urls import path
from django.contrib.auth import views as auth_views

from tasktodo.settings import LOGIN_URL
from tasks import views
from .constants import RouteGroup  # adjust import path if needed

# URL patterns for the tasks application
urlpatterns = [
    # Public URLs
    path('register/', views.RegisterView.as_view(), name=RouteGroup.AUTH.REGISTER.url_name),
    path('login/', auth_views.LoginView.as_view(template_name=RouteGroup.AUTH.LOGIN.template_path, redirect_authenticated_user=True), name=RouteGroup.AUTH.LOGIN.url_name),
    path('logout/', auth_views.LogoutView.as_view(), name=RouteGroup.AUTH.LOGOUT.url_name),
    path('', views.HomeView.as_view(), name=RouteGroup.PROTECTED.HOME.url_name),
    path('tasks/', views.ListTaskView.as_view(), name=RouteGroup.PROTECTED.TASKS.LIST.url_name),
]
