from django import forms
from django.forms import widgets

from webapp.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'type': widgets.CheckboxSelectMultiple,
            'description': widgets.Textarea(attrs={"placeholder": 'Input full description of your task'})
        }

