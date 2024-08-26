from datetime import datetime
import category
from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from django.http import JsonResponse, Http404
from rest_framework.decorators import api_view, action
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from tasks.models import *
from tasks.serializers import *
from rest_framework.pagination import PageNumberPagination, CursorPagination
from django.db.models import Count
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


# class TaskPagination(PageNumberPagination): # Использование класса пагинации 1 способ
#     page_size = 2 # Количество элементов на странице
#     page_size_query_param = 'page_size'
#     max_page_size = 20


# class SubTaskPagination(PageNumberPagination): # Использование класса пагинации 1 способ
#     page_size = 2 # Количество элементов на странице
#     page_size_query_param = 'page_size'
#     max_page_size = 20


# class TaskCursorPagination(CursorPagination):
#     page_size = 2
#     ordering = 'title' # Поле для курсора

def set_jwt_cookies(response, user):
    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token
    # Устанавливает JWT токены в куки.
    access_expiry = datetime.utcfromtimestamp(access_token['exp'])
    refresh_expiry = datetime.utcfromtimestamp(refresh_token['exp'])
    response.set_cookie(
        key='access_token',
        value=str(access_token),
        httponly=True,
        secure=False,
        samesite='Lax',
        expires=access_expiry
    )
    response.set_cookie(
        key='refresh_token',
        value=str(refresh_token),
        httponly=True,
        secure=False,
        samesite='Lax',
        expires=refresh_expiry
    )


class TaskListCreateAPIView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # pagination_class = TaskPagination  # Использование класса пагинации 1 способ
    # pagination_class = TaskCursorPagination  # Использование класса пагинации CursorPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']


class TaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class SubTaskListCreateAPIView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    # pagination_class = SubTaskPagination  # Использование класса пагинации 1 способ
    # pagination_class = TaskCursorPagination  # Использование класса пагинации CursorPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']


class SubTaskDetailUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer


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


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False, methods=['get'])
    def count_tasks(self, request):
        categories_with_task_counts = Category.objects.annotate(task_count=Count('task'))

        data = [
            {
                "id": category.id,
                "category": category.name,
                "task_count": category.task_count
            }
            for category in categories_with_task_counts
        ]
        return Response(data)


class SubTaskListCreateView(APIView):
    def get(self, request):
        subtasks = SubTask.objects.all()
        serializer = SubTaskSerializer(subtasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SubTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):
    def get_object(self, pk):
        try:
            return SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        subtask = self.get_object(pk)
        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        subtask = self.get_object(pk)
        serializer = SubTaskSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = self.get_object(pk)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            # Используем exp для установки времени истечения куки
            access_expiry = datetime.utcfromtimestamp(access_token['exp'])
            refresh_expiry = datetime.utcfromtimestamp(refresh['exp'])
            response = Response(status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=str(access_token),
                httponly=True,
                secure=False,  # Используйте True для HTTPS
                samesite='Lax',
                expires=access_expiry
            )
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=False,
                samesite='Lax',
                expires=refresh_expiry
            )
            return response
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


class ProtectedDataView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Hello, authenticated user!", "user": request.user.username})


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response = Response({
                'user': {
                    'username': user.username,
                    'email': user.email
                }
            }, status=status.HTTP_201_CREATED)
            set_jwt_cookies(response, user)
            return response
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "This is accessible by anyone!"})


class PrivateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Hello, {request.user.username}!"})


class AdminView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({"message": "Hello, Admin!"})


class ReadOnlyOrAuthenticatedView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        return Response({"message": "This is readable by anyone, but modifiable only by authenticated users."})

    def post(self, request):
        return Response({"message": "Data created by authenticated user!"})