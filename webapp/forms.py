from django import forms
from django.forms import widgets

from webapp.models import Type, Status, Task


class TaskForm(forms.Form):
    summary = forms.CharField(max_length=50, required=True, label='Summary')
    description = forms.CharField(max_length=500, required=False, label='Description',
                                  widget=widgets.Textarea(attrs={"cols": 40, "rows": 3}))
    type = forms.ModelMultipleChoiceField(queryset=Type.objects.all(), required=True, label='Type')
    status = forms.ModelChoiceField(queryset=Status.objects.all())
