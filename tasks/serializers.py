from rest_framework import serializers
from rest_framework.authtoken.admin import User
from rest_framework.exceptions import ValidationError

from .models import *
from django.utils import timezone


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['owner'] # Автоматическое добавление владельца объекта


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task

    def validate_deadline(self, value): # Проверка, что deadline не в прошлом.
        if value < timezone.now():
            raise ValidationError("Дата выполнения задачи не может быть в прошлом.")
        return value


class TaskCreateUpdateSerializer(TaskSerializer):
    # Используется для создания новой или обновления сцществующей задачи. Включает только указанные поля.
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline']

    # Добавляет текущую дату в поле created_at перед созданием объекта:
    def create(self, validated_data):
        validated_data['created_at'] = timezone.now()
        return super().create(validated_data)


class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ['created_at']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__' # Включаем все поля модели Category

    def validate_name(self, value):
        # Проверка, существует ли уже категория с таким названием
        if Category.objects.filter(name=value).exists():
            raise ValidationError("Категория с таким названием уже существует.")
        return value

    def create(self, validated_data):
        # Используем validate_name для проверки уникальности при создании
        self.validate_name(validated_data.get['name'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Используем validate_name для проверки уникальности при обновлении
        # Проверяем, не совпадает ли имя с текущим именем категории
        if 'name' in validated_data and validated_data['name'] != instance.name:
            self.validate_name(validated_data.get['name'])
        return super().update(instance, validated_data)


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'  # Включить все поля модели SubTask


class TaskDetailSerializer(serializers.ModelSerializer):
    # Вложенный сериализатор для отображения всех подзадач,
    # связанных с данной задачей. Параметр many=True указывает,
    # что может быть несколько подзадач. Параметр read_only=True
    # указывает, что это поле доступно только для чтения.
    subtasks = SubTaskSerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = '__all__' # Включить все поля модели Task и вложенные подзадачи

    def to_representation(self, instance):
        # Метод используется для кастомизации отображаемых данных.
        # Здесь дополнительно сериализируются все подзадачи, связанные с задачей,
        # и добавляются в вывод.
        representation = super().to_representation(instance)
        # Получаем связанные подзадачи
        representation['subtasks'] = SubTaskSerializer(instance.subtasks.all(), many=True).data
        return representation


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user
