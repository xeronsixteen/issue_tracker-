from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import ProjectForm
from webapp.models import Project


class ProjectView(ListView):
    template_name = 'projects/projects.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.all().order_by('-created_at')


class OneProjectView(DetailView):
    template_name = "projects/one_project_view.html"
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.object.tasks.order_by("-created_at")
        return context


class CreateProject(CreateView):
    form_class = ProjectForm
    template_name = "projects/create.html"

    def get_success_url(self):
        return reverse('project_view', kwargs={"pk": self.object.pk})


class UpdateProject(UpdateView):
    form_class = ProjectForm
    template_name = "projects/update.html"
    model = Project

    def get_success_url(self):
        return reverse('project_list')


class DeleteProject(DeleteView):
    model = Project

    def get(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('project_list')
