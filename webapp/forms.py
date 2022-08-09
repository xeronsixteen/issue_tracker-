from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import widgets, EmailField

from webapp.models import Task, Project


class TaskForm2(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['project']
        widgets = {
            'type': widgets.CheckboxSelectMultiple,
            'description': widgets.Textarea(attrs={"placeholder": 'Input full description of your task'}),
            'status': widgets.RadioSelect
        }

    def clean_summary(self):
        summary = self.cleaned_data.get('summary')
        if len(summary) <= 4:
            raise ValidationError('Please, enter more than 4 symbols')
        if Task.objects.filter(summary=summary).exists():
            raise ValidationError('A task with that name exists')
        # if not re.match('ˆ[a-zA-Zа-яА-Я\s]+$', summary):
        #     raise ValidationError ('Please, enter only letters')
        return summary

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) > 2000:
            raise ValidationError('Max length of description is 2000')
        if Task.objects.filter(description=description).exists():
            raise ValidationError('A description with that name exists')
        return description

    def clean(self):
        if self.cleaned_data.get('summary') == self.cleaned_data.get('description'):
            raise ValidationError('Summary and description could not be the same')
        return super().clean()


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'type': widgets.CheckboxSelectMultiple,
            'description': widgets.Textarea(attrs={"placeholder": 'Input full description of your task'}),
            'status': widgets.RadioSelect
        }

    def clean_summary(self):
        summary = self.cleaned_data.get('summary')
        if len(summary) <= 4:
            raise ValidationError('Please, enter more than 4 symbols')
        if Task.objects.filter(summary=summary).exists():
            raise ValidationError('A task with that name exists')
        # if not re.match('ˆ[a-zA-Zа-яА-Я\s]+$', summary):
        #     raise ValidationError ('Please, enter only letters')
        return summary

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) > 2000:
            raise ValidationError('Max length of description is 2000')
        if Task.objects.filter(description=description).exists():
            raise ValidationError('A description with that name exists')
        return description

    def clean(self):
        if self.cleaned_data.get('summary') == self.cleaned_data.get('description'):
            raise ValidationError('Summary and description could not be the same')
        return super().clean()


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='Find')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'created_at': widgets.SelectDateWidget,
            'finished_at': widgets.SelectDateWidget,
        }


class MyUserCreationForm(UserCreationForm):
    email = EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2',
                  'first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('Такое мыло существует в БД')
        return email

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('Такое имя существует в БД')
        return username

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data['first_name'].strip()
        last_name = cleaned_data['last_name'].strip()
        if not first_name and not last_name:
            raise ValidationError('Заполните хотя бы одно из полей : имя или фамилия')

