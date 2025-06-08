from django.urls import path
from tasks import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('', views.list_tasks, name='tasks'),
]