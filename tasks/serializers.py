from django.contrib.auth import get_user_model
from rest_framework import serializers

from spareparts.serializers import PlannedSparepartSerializer
from .models import Task


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email']


class TaskCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
        extra_kwargs = {'author': {'required': False}}


class TaskListSerializer(serializers.ModelSerializer):

    author = UserSerializer()
    assigned = UserSerializer()
    spareparts = PlannedSparepartSerializer(source='plannedsparepart_set', many=True)

    class Meta:
        model = Task
        fields = '__all__'


class TaskChangeStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['status']
        extra_kwargs = {'status': {'required': True}}
