from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView

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

    def form_valid(self, form):
        # project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        project = form.save(commit=False)
        project.save()
        form.save_m2m()
        return redirect('project_view', pk=project.pk)


