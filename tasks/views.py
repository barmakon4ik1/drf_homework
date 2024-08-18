from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count


# Представление для всех задач GET и POST:
@api_view(['GET', 'POST'])
def task_list_create(request):
    if request.method == 'GET':
        # Получает все объекты Task из базы данных:
        tasks = Task.objects.all()
        total_tasks = Task.objects.count()
        sum_by_status = Task.objects.values('status').annotate(sum_by_status=Count('id'))
        overdue = Task.objects.filter(deadline__lte=timezone.now()).count()

        # Сериализует все объекты task с использованием TaskSerializer:
        serializer = TaskSerializer(tasks, many=True)

        # Возвращает сериализованные данные с HTTP-статусом 200_ОК:
        return Response({
            'total_tasks': total_tasks,
            'sum_by_status': sum_by_status,
            'overdue_tasks': overdue,
            'tasks': serializer.data
        }, status=status.HTTP_200_OK
        )

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


def task_list(request):
    status = request.GET.get('status')
    deadline = request.GET.get('deadline')
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)

    tasks = Task.objects.all()

    if status:
        tasks = tasks.filter(status=status)

    if deadline:
        tasks = tasks.filter(deadline__lte=deadline)

    paginator = Paginator(tasks, page_size)
    page_obj = paginator.get_page(page_number)

    tasks_data = [
        {
            "id": task.id,
            "title": task.title,
            "status": task.status,
            "deadline": task.deadline,
        }
        for task in page_obj
    ]

    return JsonResponse({
            "tasks": tasks_data,
            "total_pages": paginator.num_pages,
            "current_page": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
        })

    """
    sum_by_status = Task.objects.values('status').annotate(sum_by_status=Count('id'))
    sum_end_deadline = Task.objects.filter(deadline__lte=timezone.now()).aggregate(sum_by_deadline=Count('id'))
    print(f'Общее количество задач: {aggregates["total_tasks"]}')
    for stat in sum_by_status:
        print(f'Статус: {stat["status"]}, Количество задач: {stat["sum_by_status"]}')
    print(f'Общее количество просроченных задач: {sum_end_deadline["sum_by_deadline"]}')"""