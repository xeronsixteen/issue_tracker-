from django.contrib.auth import login, get_user_model
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView

from accounts.forms import MyUserCreationForm


class RegisterView(CreateView):
    model = User
    template_name = 'registration/registration.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
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


class UserDetailView(DetailView):
    template_name = 'registration/user.html'
    model = get_user_model()
    context_object_name = 'user'
