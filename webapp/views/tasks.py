from urllib import request

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView

from webapp.forms import TaskForm, SearchForm
from webapp.models import Task


# Create your views here.

class IndexView(ListView):
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


class TaskView(TemplateView):
    template_name = "tasks/task_view.html"

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        task = get_object_or_404(Task, pk=pk)
        kwargs["task"] = task
        return super().get_context_data(**kwargs)


class TaskCreateView(View):
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
            return redirect('task_list')
        return render(request, 'tasks/create.html', {'form': form})


class TaskUpdateView(UpdateView):
    form_class = TaskForm
    template_name = 'tasks/update.html'
    model = Task

    def get_success_url(self):
        return reverse('task_view', kwargs={'pk': self.object.pk})


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('task_list')






