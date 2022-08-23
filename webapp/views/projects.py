from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import ProjectForm, UserForm
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
        project = form.save()
        user_id = self.request.user
        project.user.add(user_id)
        project.save()
        return super().form_valid(form)

    def has_permission(self):
        return self.request.user.has_perm(
            'webapp.add_project') or self.request.user == self.get_object().user


class AddUserInProject(PermissionRequiredMixin, UpdateView):
    model = Project
    template_name = 'projects/AddUser.html'
    form_class = UserForm
    context_object_name = 'project'
    permission_required = 'webapp.change_project'

    def form_valid(self, form):
        # pk = self.kwargs.get('pk')
        # project= get_object_or_404(Project,pk = pk)
        project = form.save()
        user_id = self.request.POST.get('user')
        author = self.request.user.pk
        project.user.add(user_id, author)
        project.save()
        return redirect('webapp:project_view', pk=project.pk)


class UpdateProject(PermissionRequiredMixin, UpdateView):
    model = Project
    template_name = 'projects/update.html'
    form_class = ProjectForm
    context_object_name = 'project'
    permission_required = 'webapp.change_project'

    def get_success_url(self):
        return reverse('webapp:project_list')

    def has_permission(self):
        return self.request.user.has_perm(
            'webapp.change_project') or self.request.user == self.get_object().user


class DeleteProject(PermissionRequiredMixin, DeleteView):
    model = Project
    context_object_name = 'project'
    template_name = 'projects/delete.html'
    success_url = reverse_lazy('webapp:project_list')
    permission_required = 'webapp.delete_project'

    # def get(self, request, *args, **kwargs):
    #     return super().delete(request, *args, **kwargs)
    #
    # def get_success_url(self):
    #     return reverse('webapp:project_list')
    #
    # def has_permission(self):
    #     return self.request.user.has_perm(
    #         'webapp.delete_project') or self.request.user == self.get_object().user
