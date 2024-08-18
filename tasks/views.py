from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer


# @api_view(['GET']): Указывает, что функция task_list обрабатывает только # GET՞запросы:
@api_view(['GET'])
def task_list(request):

    # Получает все объекты Task из базы данных:
    tasks = Task.objects.all()

    # Сериализует все объекты task с использованием TaskSerializer:
    serializer = TaskSerializer(tasks, many=True)

    # Возвращает сериализованные данные с HTTP-статусом 200_ОК:
    return Response(serializer.data, status=status.HTTP_200_OK)
