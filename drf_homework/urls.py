from django.contrib import admin
# from django.contrib.auth.views import LoginView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasks.views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="First API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@local.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)


urlpatterns = [

    path('admin/', admin.site.urls),

    path('protected/', ProtectedDataView.as_view(), name='protected-data'),
    # Пагинация и фильтры:
    path('tasks/', TaskListCreateAPIView.as_view(), name='tasks'),
    path('subtasks/', SubTaskListCreateAPIView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteAPIView.as_view(), name='subtask-detail-update-delete'),


    # Для получения всех задач и создания новой:
    path('task/', task_list_create, name='task-list-create'),
    # Для операции с одной задачей
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view(),
         name='task-detail-update-delete'),
    path('user-tasks', UserTaskListView.as_view(), name='user-tasks'),

    # # JSon с пагинацией
    # path('info/', task_list, name='task_list'),
    path('subtasks-API/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks-API/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),

    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/', ReadOnlyOrAuthenticatedView.as_view(), name='admin'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('', include(router.urls))

]
