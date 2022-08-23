from django.urls import path

from webapp.views import IndexView, TaskView, TaskUpdateView, TaskDeleteView, TaskCreateView, TaskCreateInProjectView
from webapp.views.projects import ProjectView, OneProjectView, CreateProject, UpdateProject, DeleteProject, \
    AddUserInProject

app_name = 'webapp'


urlpatterns = [
    path('tasks/', IndexView.as_view(), name="task_list"),
    path('task/<int:pk>/', TaskView.as_view(), name="task_view"),
    path('tasks/add/', TaskCreateView.as_view(), name="create"),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name="update"),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name="delete"),
    path('', ProjectView.as_view(), name='project_list'),
    path('project/<int:pk>/', OneProjectView.as_view(), name='project_view'),
    path('project/add/', CreateProject.as_view(), name="create_project"),
    path('project/<int:pk>/update/', UpdateProject.as_view(), name="update_project"),
    path('project/<int:pk>/delete/', DeleteProject.as_view(), name="delete_project"),
    path('project/<int:pk>/task/add', TaskCreateInProjectView.as_view(), name="TaskCreateInProjectView"),
    path('projects/<int:pk>/user/add', AddUserInProject.as_view(), name='AddUserInProject')
]


