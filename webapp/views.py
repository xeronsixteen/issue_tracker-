from urllib import request


from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.http import urlencode
from django.views import View
from django.views.generic import TemplateView, ListView

from webapp.forms import TaskForm, SearchForm
from webapp.models import Task


# Create your views here.

class IndexView(ListView):
    template_name = 'index.html'
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
    template_name = "task_view.html"

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        task = get_object_or_404(Task, pk=pk)
        kwargs["task"] = task
        return super().get_context_data(**kwargs)


class CreateView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        form = TaskForm
        return render(request, "create.html", {'form': form})

    @staticmethod
    def post(request, *args, **kwargs):
        form = TaskForm(data=request.POST)
        if form.is_valid():
            summary = form.cleaned_data.get('summary')
            description = form.cleaned_data.get('description')
            status = form.cleaned_data.get('status')
            type = form.cleaned_data.get('type')
            new_task = Task.objects.create(summary=summary, description=description, status=status)
            new_task.type.set(type)
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
            'type': self.task.type.all()
        })
        return render(request, "update.html", {'form': form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(data=request.POST)
        if form.is_valid():
            self.task.summary = form.cleaned_data.get('summary')
            self.task.description = form.cleaned_data.get('description')
            self.task.status = form.cleaned_data.get('status')
            self.task.type.set(form.cleaned_data.get('type'))
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
