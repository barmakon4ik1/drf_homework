from django.urls import path
from tasks.views import task_list

urlpatterns = [
    path('tasks/', task_list, name='task-list'), # маршрут для получения всех задач
]
