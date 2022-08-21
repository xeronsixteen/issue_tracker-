from urllib import request

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView

from webapp.forms import TaskForm, SearchForm, TaskForm2
from webapp.models import Task, Project


# Create your views here.

class IndexView(LoginRequiredMixin, ListView):
    template_name = 'tasks/index.html'
    model = Task
    context_object_name = 'tasks'
    ordering = 'updated_at'
    paginate_by = 5

    def get(self, *args, **kwargs):
        self.form = self.get_search_form()
        self.get_search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.get_search_value:
            return Task.objects.filter(Q(summary__icontains=self.get_search_value) | Q(
                description__icontains=self.get_search_value))
        return Task.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.get_search_value:
            query = urlencode({'search': self.get_search_value})
            context['query'] = query
            context['search'] = self.get_search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


class TaskView(LoginRequiredMixin, TemplateView):
    template_name = "tasks/task_view.html"

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        task = get_object_or_404(Task, pk=pk)
        kwargs["task"] = task
        return super().get_context_data(**kwargs)


class TaskCreateInProjectView(LoginRequiredMixin, CreateView):
    form_class = TaskForm2
    template_name = "tasks/createinproject.html"

    # model = Task

    def get_success_url(self):
        return reverse("webapp:task_view", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        task = form.save(commit=False)
        task.project = project
        task.save()
        form.save_m2m()
        return redirect('webapp:project_view', pk=project.pk)


class TaskCreateView(LoginRequiredMixin, View):
    @staticmethod
    def get(request, *args, **kwargs):
        form = TaskForm
        return render(request, "tasks/create.html", {'form': form})

    @staticmethod
    def post(request, *args, **kwargs):
        form = TaskForm(data=request.POST)
        if form.is_valid():
            summary = form.cleaned_data.get('summary')
            description = form.cleaned_data.get('description')
            status = form.cleaned_data.get('status')
            type = form.cleaned_data.get('type')
            project = form.cleaned_data.get('project')
            new_task = Task.objects.create(summary=summary, description=description, status=status, project=project)
            new_task.type.set(type)
            return redirect('webapp:project_list')
        return render(request, 'tasks/create.html', {'form': form})

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:task_view', kwargs={'pk': self.object.pk})

    # def has_permission(self):
    #     return self.request.user.has_perm(
    #         'webapp.add_task') or self.request.user == self.object().user


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    form_class = TaskForm
    template_name = 'tasks/update.html'
    model = Task

    def get_success_url(self):
        return reverse('webapp:task_view', kwargs={'pk': self.object.pk})

    def has_permission(self):
        return self.request.user.has_perm(
            'webapp.change_task') or self.request.user == self.get_object().user


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('webapp:task_list')

    def has_permission(self):
        return self.request.user.has_perm(
            'webapp.delete_task') or self.request.user == self.get_object().user
