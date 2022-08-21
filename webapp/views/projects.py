from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import ProjectForm
from webapp.models import Project


class ProjectView(LoginRequiredMixin, ListView):
    template_name = 'projects/projects.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.all().order_by('-created_at')


class OneProjectView(LoginRequiredMixin, DetailView):
    template_name = "projects/one_project_view.html"
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.object.tasks.order_by("-created_at")
        return context


class CreateProject(PermissionRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = "projects/create.html"

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)

    def has_permission(self):
        return self.request.user.has_perm(
            'webapp.add_project') or self.request.user == self.get_object().user


class UpdateProject(LoginRequiredMixin, UpdateView):
    form_class = ProjectForm
    template_name = "projects/update.html"
    model = Project

    def get_success_url(self):
        return reverse('webapp:project_list')

    def has_permission(self):
        return self.request.user.has_perm(
            'webapp.change_project') or self.request.user == self.get_object().user


class DeleteProject(LoginRequiredMixin, DeleteView):
    model = Project

    def get(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:project_list')

    def has_permission(self):
        return self.request.user.has_perm(
            'webapp.delete_project') or self.request.user == self.get_object().user
