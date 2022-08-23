from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView

from accounts.forms import MyUserCreationForm
from accounts.models import Profile


class RegisterView(CreateView):
    model = User
    template_name = 'registration/registration.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('webapp:task_list')

        return next_url


class UsersView(ListView):
    template_name = 'registration/users.html'
    model = get_user_model()
    context_object_name = 'users'


class UserDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'registration/user.html'
    context_object_name = 'user_obj'
    paginate_related_by = 5
    paginate_related_orphans = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = self.object.projects.order_by('-created_at')
        paginator = Paginator(projects, self.paginate_related_by, orphans=self.paginate_related_orphans)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        context['page_obj'] = page
        context['projects'] = page.object_list
        context['is_paginated'] = page.has_other_pages()
        return context
