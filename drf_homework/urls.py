from django.contrib import admin
# from django.contrib.auth.views import LoginView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasks.views import *


router = DefaultRouter()
router.register(r'categories', CategoryViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    # Пагинация и фильтры:
    path('task/', TaskListCreateAPIView.as_view(), name='tasks'),
    path('subtasks/', SubTaskListCreateAPIView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteAPIView.as_view(), name='subtask-detail-update-delete'),


    # Для получения всех задач и создания новой:
    path('tasks/', task_list_create, name='task-list-create'),
    # Для операции с одной задачей
    path('tasks/<int:pk>/', task_detail_update_delete, name='task-detail-update-delete'),

    # # JSon с пагинацией
    # path('info/', task_list, name='task_list'),
    path('subtasks-API/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks-API/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),

    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/', ReadOnlyOrAuthenticatedView.as_view(), name='admin')
]
