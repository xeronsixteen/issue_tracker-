from django import forms
from django.forms import widgets

from webapp.models import Type, Status


class TaskForm(forms.Form):
    summary = forms.CharField(max_length=50, required=True, label='Name')
    description = forms.CharField(max_length=500, required=True, label='Text', widget=widgets.Textarea(attrs={"cols":
                                                                                                                  40,
                                                                                                      "rows": 3}))
    type = forms.ModelChoiceField(queryset=Type.objects.all())
    status = forms.ModelChoiceField(queryset=Status.objects.all())