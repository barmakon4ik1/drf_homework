from django.contrib import admin
from django.urls import path
from tasks.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # Для получения всех задач и создания новой:
    path('tasks/', task_list_create, name='task-list-create'),

    # Для операции с одной задачей
    path('tasks/<int:pk>/', task_detail_update_delete, name='task-detail-update-delete'),

    # JSon с пагинацией
    path('task/', task_list, name='task_list'),

]
