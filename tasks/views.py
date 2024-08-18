from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# from .models import Task
from .serializers import *


# Представление для всех задач GET и POST:
@api_view(['GET', 'POST'])
def task_list_create(request):
    if request.method == 'GET':
        # Получает все объекты Task из базы данных:
        tasks = Task.objects.all()

        # Сериализует все объекты task с использованием TaskSerializer:
        serializer = TaskSerializer(tasks, many=True)

        # Возвращает сериализованные данные с HTTP-статусом 200_ОК:
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Инициализирует сериализатор с данными из запроса:
        serializer = TaskCreateUpdateSerializer(data=request.data)

        if serializer.is_valid():  # Проверяет валидность данных
            serializer.save()  # Сохраняет новый объект, вызывая переопределенный метод create.

            # Возвращает сериализованные данные новой задачи с HTTP статусом 201-Created):
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Возвращает ошибки валидации с HTTP статусом 400 Bad Request):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Представление для одной задачи GET, PUT, DELETE
@api_view(['GET', 'PUT', 'DELETE'])
def task_detail_update_delete(request, pk):
    try:
        # Пытается найти задачу с заданным первичным  ключом. Если она не найдена, возвращает ошибку 404 Not Found.
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Сериализует все объекты task с использованием TaskSerializer:
        serializer = TaskSerializer(task)

        # Возвращает сериализованные данные с HTTP-статусом 200_ОК:
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        # Инициализирует сериализатор с данными запроса и существующим объектом задачи
        serializer = TaskCreateUpdateSerializer(task, data=request.data)

        if serializer.is_valid():  # Проверяет валидность данных.
            serializer.save()  # Сохраняет обновленный объект задачи, вызывая переопределенный метод update.
            # Возвращает сериализованные данные обновленной задачи с HTTP статусом 200 Ok):
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Возвращает ошибки валидации с HTTP статусом 400 Bad Request):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()  # Удаляет найденный объект из базы данных

        # Возвращает сообщение об успешном удалении с HTTP статусом 204 No Content)
        return Response({'message': 'Task deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

