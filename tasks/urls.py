from django.urls import path

from .views import TasksListCreateAPIView, TaskChangeStatusAPIView


urlpatterns = [
    path('', TasksListCreateAPIView.as_view(), name='tasks-list-create'),
    path('change-status/<int:pk>/', TaskChangeStatusAPIView.as_view(), name='tasks-change-status'),
]
