from django.db import models


class Task(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    ]
    title = models.CharField(max_length=120)
    description = models.TextField()
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default='NEW')
    deadline = models.DateField()

    def __str__(self):
        return self.title

