from django.urls import path

from webapp.views import IndexView, TaskView, UpdateView, DeleteView, CustomCreateView
from webapp.views.projects import ProjectView, OneProjectView, CreateProject

urlpatterns = [
    path('tasks/', IndexView.as_view(), name="task_list"),
    path('task/<int:pk>/', TaskView.as_view(), name="task_view"),
    path('tasks/add/', CustomCreateView.as_view(), name="create"),
    path('task/<int:pk>/update/', UpdateView.as_view(), name="update"),
    path('task/<int:pk>/delete/', DeleteView.as_view(), name="delete"),
    path('', ProjectView.as_view(), name='project_list'),
    path('project/<int:pk>/', OneProjectView.as_view(), name='project_view'),
    path('project/add/', CreateProject.as_view(), name="create_project"),
]
