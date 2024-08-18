from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskCreateUpdateSerializer(TaskSerializer):
    # Используется для создания новой или обновления сцществующей задачи. Включает только указанные поля.
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline']
