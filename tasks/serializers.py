from rest_framework import serializers
from .models import Task
from django.utils import timezone


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskCreateUpdateSerializer(TaskSerializer):
    # Используется для создания новой или обновления сцществующей задачи. Включает только указанные поля.
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline']

    # Добавляет текущую дату в поле created_at перед созданием объекта:
    def create(self, validated_data):
        validated_data['created_at'] = timezone.now()
        return super().create(validated_data)



