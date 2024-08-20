from django.contrib import admin
from django.urls import path
from tasks.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # Пагинация и фильтры:
    path('task/', TaskListCreateAPIView.as_view(), name='tasks'),


    # Для получения всех задач и создания новой:
    path('tasks/', task_list_create, name='task-list-create'),
    # Для операции с одной задачей
    path('tasks/<int:pk>/', task_detail_update_delete, name='task-detail-update-delete'),

    # # JSon с пагинацией
    # path('info/', task_list, name='task_list'),

]
