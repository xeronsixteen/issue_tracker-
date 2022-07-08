from django.db import models

# Create your models here.

TYPE_CHOICES = [('task', 'Task'), ('bug', 'Bug'), ('enhancement', 'Enhancement')]
STATUS_CHOICES = [('new', 'New'), ('in_progress', 'In progress'), ('done', 'Done')]


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="date of creation")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="date of update")


class Task(BaseModel):
    summary = models.CharField(max_length=100, verbose_name='summary')
    description = models.TextField(max_length=2000, null=False, blank=True, verbose_name='description')
    status = models.ForeignKey('webapp.Status', on_delete=models.PROTECT, related_name='statuses',
                               verbose_name='status')
    type = models.ForeignKey('webapp.Type', on_delete=models.PROTECT, related_name='types', verbose_name='type')

    def __str__(self):
        return f"{self.id}. {self.summary}: {self.description}"

    class Meta:
        db_table = "tasks"
        verbose_name = "Task"
        verbose_name_plural = "Tasks"


class Type(BaseModel):
    name = models.CharField(max_length=50, null=False, blank=False,
                            verbose_name='type', default=STATUS_CHOICES[0][0], choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.id}. {self.name}"

    class Meta:
        db_table = "types"
        verbose_name = "Type"
        verbose_name_plural = "Types"


class Status(BaseModel):
    name = models.CharField(max_length=50, null=False, blank=False,
                            verbose_name='status', default=TYPE_CHOICES[0][0], choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.id}. {self.name}"

    class Meta:
        db_table = "statuses"
        verbose_name = "Status"
        verbose_name_plural = "Statuses"
