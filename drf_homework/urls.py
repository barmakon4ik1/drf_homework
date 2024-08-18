from django.urls import path
from tasks.views import task_list_create, task_detail_update_delete

urlpatterns = [
    # Для получения всех задач и создания новой:
    path('tasks/', task_list_create, name='task-list-create'),

    # Для операции с одной задачей
    path('tasks/<int:pk>/', task_detail_update_delete, name='task-detail-update-delete'),
]
