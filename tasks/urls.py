from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .constants import Urls, Templates  # adjust import path if needed

# URL patterns for the tasks application
urlpatterns = [
    # Public URLs
    path(
        'register/',
        views.RegisterView.as_view(),
        name=Urls.AUTH.REGISTER
    ),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name=Templates.AUTH.LOGIN,
            redirect_authenticated_user=True
        ),
        name=Urls.AUTH.LOGIN
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name=Urls.AUTH.LOGOUT # You can make this a constant too, if reused
    ),

    # Protected URLs
    path(
        '',
        views.HomeView.as_view(),
        name=Urls.PROTECTED.HOME
    ),

    # Task URLs
    path(
        'tasks/',
        views.ListTaskView.as_view(),
        name=Urls.PROTECTED.TASKS # You can also define this in a _TaskUrls class
    ),
]
