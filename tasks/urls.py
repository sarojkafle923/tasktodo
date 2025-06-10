from django.urls import path
from django.contrib.auth import views as auth_views
from tasks import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True # Redirects authenticated users to the tasks page        
    ),
         name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'  # Redirects to login page after logout
    ), name='logout'),
    path('', views.list_task, name='tasks'),
]