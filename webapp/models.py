from django.db import models


# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="date of creation")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="date of update")

    class Meta:
        abstract = True


class Task(BaseModel):
    summary = models.CharField(max_length=100, verbose_name='summary')
    description = models.TextField(null=False, blank=True, verbose_name='description')
    status = models.ForeignKey('webapp.Status', on_delete=models.PROTECT, related_name='tasks',
                               verbose_name='status')

    type = models.ManyToManyField('webapp.Type', related_name='tasks', through='TaskType',
                                  through_fields=('task', 'type'), blank=False)

    def __str__(self):
        return f"{self.id}. {self.summary}: {self.description}"

    class Meta:
        db_table = "tasks"
        verbose_name = "Task"
        verbose_name_plural = "Tasks"


class Status(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name='status')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "statuses"
        verbose_name = "Status"
        verbose_name_plural = "Statuses"


class Type(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name='type')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "types"
        verbose_name = "Type"
        verbose_name_plural = "Types"


class TaskType(models.Model):
    task = models.ForeignKey('webapp.Task',
                             related_name='task_types',
                             on_delete=models.CASCADE,
                             verbose_name='Task')

    type = models.ForeignKey('webapp.Type',
                             related_name='type_tasks',
                             on_delete=models.CASCADE,
                             verbose_name='Type')
