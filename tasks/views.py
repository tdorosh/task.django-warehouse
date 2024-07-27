from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskChangeStatusSerializer, TaskCreateSerializer, TaskListSerializer


class TasksListCreateAPIView(generics.ListCreateAPIView):

    queryset = Task.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'POST':
            serializer_class = TaskCreateSerializer
        return serializer_class

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TaskChangeStatusAPIView(generics.UpdateAPIView):

    queryset = Task.objects.all()
    serializer_class = TaskChangeStatusSerializer
    permission_classes = [IsAuthenticated]
