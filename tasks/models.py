from django.db import models
# from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from .variables import *


class Task(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Наименование задачи',
        unique=True
    )
    description = models.TextField(verbose_name="Описание задачи")
    categories = models.ManyToManyField('Category')
    status = models.CharField(
        max_length=15,
        choices=Task_name.task_choices,
        default=Task_name.NEW,
        verbose_name="Тип задачи"
    )
    deadline = models.DateTimeField(verbose_name="Срок выполнения")
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время начала выполнения"
    )


    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        constraints = [
            models.UniqueConstraint(
                fields=['title'],
                name='unique_task'
            )  # Уникальность по полю 'title'
        ]


class SubTask(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Наименование подзадачи',
        unique=True
    )
    description = models.TextField(verbose_name="Описание подзадачи")
    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        verbose_name='Основная задача'
    )
    status = models.CharField(
        max_length=15,
        choices=Task_name.task_choices,
        default=Task_name.NEW,
        verbose_name="Тип подзадачи"
    )
    deadline = models.DateTimeField(verbose_name="Срок выполнения")
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время начала выполнения"
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'Subtask'
        verbose_name_plural = 'Subtasks'
        constraints = [
            models.UniqueConstraint(
                fields=['title'],
                name='unique_subtask'
            )
        ]


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Наименование категории")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

