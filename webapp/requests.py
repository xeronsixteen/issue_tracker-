from datetime import datetime, timedelta

from django.db.models import Q

from webapp.models import Task

#first task
Task.objects.filter(created_at__gte=datetime.now()-timedelta(days=30)).filter(status__name__istartswith='Done')

#second_task
q1 = Q(status__name__in=('New', 'In Progress'))
q2 = Q(type__name__in=('Bug', 'tasks'))
Task.objects.filter(q1 & q2)

#third_task
q3 = Q(type__name='Bug')
q4 = Q(status__name='New')
q5 = Q(status__name='In Progress')
Task.objects.filter(q3 | q4 | q5)






