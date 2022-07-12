from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView

from webapp.forms import TaskForm
from webapp.models import Task


# Create your views here.

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        tasks = Task.objects.order_by('description')
        kwargs["tasks"] = tasks
        return super().get_context_data(**kwargs)


class TaskView(TemplateView):
    template_name = "task_view.html"

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        task = get_object_or_404(Task, pk=pk)
        kwargs["task"] = task
        return super().get_context_data(**kwargs)


class CreateView(View):
    def get(self, request, *args, **kwargs):
        form = TaskForm
        return render(request, "create.html", {'form': form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(data=request.POST)
        if form.is_valid():
            summary = form.cleaned_data.get('summary')
            description = form.cleaned_data.get('description')
            status = form.cleaned_data.get('status')
            type = form.cleaned_data.get('type')
            new_task = Task.objects.create(summary=summary, description=description, status=status, type=type)
            return redirect('index')
        return render(request, 'create.html', {'form': form})


class UpdateView(View):
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        self.task = get_object_or_404(Task, pk=pk)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = TaskForm(initial={
            'summary': self.task.summary,
            'description': self.task.description,
            'status': self.task.status,
            'type': self.task.type
        })
        return render(request, "update.html", {'form': form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(data=request.POST)
        if form.is_valid():
            self.task.summary = form.cleaned_data.get('summary')
            self.task.description = form.cleaned_data.get('description')
            self.task.status = form.cleaned_data.get('status')
            self.task.type = form.cleaned_data.get('type')
            self.task.save()
            return redirect('index')
        return redirect('index', {'form': form})


class DeleteView(View):
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        self.task = get_object_or_404(Task, pk=pk)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, "delete.html", {"task": self.task})

    def post(self, request, *args, **kwargs):
        self.task.delete()
        return redirect('index')
