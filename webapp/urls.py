from django.urls import path

from webapp.views import IndexView, TaskView, CreateView, UpdateView, DeleteView

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('task/<int:pk>/', TaskView.as_view(), name="task_view"),
    # path('tasks/', RedirectView.as_view(pattern_name="index")),
    path('tasks/add/', CreateView.as_view(), name="create"),
    path('task/<int:pk>/update/', UpdateView.as_view(), name="update"),
    path('task/<int:pk>/delete/', DeleteView.as_view(), name="delete"),
]