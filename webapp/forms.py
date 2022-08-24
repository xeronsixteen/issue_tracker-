from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

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
    search = forms.CharField(max_length=50, required=False)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user']
        widgets = {
            'created_at': widgets.SelectDateWidget,
            'finished_at': widgets.SelectDateWidget,
        }


class ProjectFormUser(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user']


class UserForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['user']
        widgets = {'user': widgets.CheckboxSelectMultiple}
