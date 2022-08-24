from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import PasswordChangeView

from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from accounts.forms import MyUserCreationForm, UserChangeForm, ProfileChangeForm, PasswordChangeForm
from accounts.models import Profile

User = get_user_model()


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
    model = User
    context_object_name = 'users'


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
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


class ChangeProfileView(PermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = 'change_user.html'
    profile_form_class = ProfileChangeForm
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'profile_form' not in context:
            context['profile_form'] = self.profile_form_class(instance=self.get_object().profile)
        return context

    def post(self, request, *args, **kwargs):
        print(request.POST)
        print(request.FILES)
        self.object = self.get_object()
        form = self.form_class(instance=self.object, data=request.POST)
        profile_form = self.profile_form_class(instance=self.object.profile,
                                               data=request.POST,
                                               files=request.FILES)
        if form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def has_permission(self):
        return self.request.user == self.get_object()

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form, profile_form):
        form.save()
        profile_form.save()
        return redirect('accounts:profile', self.object.pk)

    def form_invalid(self, form, profile_form):
        return self.render_to_response(self.get_context_data(form=form, profile_form=profile_form))


class ChangePasswordView(PasswordChangeView):
    # model = User
    # form_class = PasswordChangeForm
    template_name = 'change_password.html'
    # context_object_name = 'user_obj'

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.request.user.pk})

