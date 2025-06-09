from django.urls import include, path
from tasks import views

urlpatterns = [
    path('', views.list_task, name='tasks'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('home/', views.home, name='home'),
]