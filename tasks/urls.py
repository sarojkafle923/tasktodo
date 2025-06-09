from django.urls import path
from tasks import views

urlpatterns = [
    path('', views.list_task, name='tasks'),
    path('register/', views.RegisterView.as_view(), name='register'),
]