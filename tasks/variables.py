from enum import Enum


class Task_name(Enum):
    NEW = 'New'
    IN_PROGRESS = 'In Progress'
    PENDING = 'Pending'
    BLOCKED = 'Blocked'
    DONE = 'Done'

    @classmethod
    def task_choices(cls):
        return [(attr.name, attr.value) for attr in cls]